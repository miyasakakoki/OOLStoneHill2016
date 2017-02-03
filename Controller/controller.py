#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ast import literal_eval

from logging import getLogger

from ryu.base import app_manager
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.controller.handler import (
    CONFIG_DISPATCHER,
    MAIN_DISPATCHER,
    set_ev_cls
)
from ryu.controller import dpset, ofp_event
from ryu.topology import switches, event
from ryu.lib import ofctl_v1_0
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.mac import haddr_to_bin
from ryu.lib.ip import ipv4_to_int


sample='sample'

class Sample(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    _CONTEXTS = { 'wsgi' : WSGIApplication }

    def __init__(self, *args, **kwargs):
        """init."""
        super(Sample, self).__init__(*args, **kwargs)
        self.log = getLogger('Sample')
        self.log.info(self.__init__.__doc__)
        self.datapathes = {}
        wsgi = kwargs['wsgi']
        wsgi.register(Rest, {sample : self})

    @set_ev_cls(event.EventSwitchEnter)
    def _switch_enter_handler(self, ev):
        """スイッチが接続されたときに発火するハンドラ．パケットインさせる"""
        self.log.info(self._switch_enter_handler.__doc__)
        datapath = ev.switch.dp
        self.datapathes[datapath] = datapath
        self.log.info("datapath is %x" % datapath.id)

        ofproto = None
        op = None
        for datapath in self.datapathes:
            parser = datapath.ofproto_parser
            proto = datapath.ofproto
            match = parser.OFPMatch(dl_type=0x0806)#, dl_src='02:00:00:00:00:01')
            actions = [     
                parser.OFPActionOutput(proto.OFPP_NORMAL)#,3 ,proto.OFP_NO_BUFFER)
            ]
        self.add_flow(datapath, 100, match, actions)
        """
        for datapath in self.datapathes:
            parser = datapath.ofproto_parser
            proto = datapath.ofproto
            match = parser.OFPMatch(dl_type=0x0806, dl_dst='02:00:00:00:00:01')
            actions = [     
                parser.OFPActionOutput(proto.OFPP_NORMAL)#,3 ,proto.OFP_NO_BUFFER)
            ]
        self.add_flow(datapath, 0, match, actions)
        """    
            
        #flow = {
        #    'match': {
        #        # Match any packets
        #    },
        #    'actions': [
        #        {
        #            'type': 'OUTPUT',
        #            'port': ofproto_v1_0.OFPP_CONTROLLER,
        #            'max_len': ofproto_v1_0.OFPCML_MAX,
        #        },
        #    ]
        #}
        # 全てのパケットをコントローラに送る．
        #ofctl_v1_0.mod_flow_entry(
        #    datapath,
        #    flow,
        #    ofproto_v1_0.OFPFC_ADD,
        #)
        

    """
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        # スイッチフィーチャーメッセージを処理する.
        # v1_0だとプロアクティブなので, トポロジ検出していないとなにもできない.
        # 今回はトポロジ検出を手動で行う, そのためすべてのパケットを通すための
        # テーブルミスフローエントリを追加する. スイッチから情報が送られてきた際に行う.
        self.log.info(self._switch_features_handler.__doc__)

        datapath = ev.msg.datapath
        self.datapathes[datapath.id] = datapath
        self.log.info('New switch is joined: %x' % datapath.id)
    """
    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """パケットインしたら全てのスイッチにNormalのFlowEntryを入れる"""
        self.log.info(self._packet_in_handler.__doc__)
        # 上がってきたパケットを出力する
        pkt = packet.Packet(ev.msg.data)
        self.log.info(pkt)
        #flow = {
        #    'match': {
        #        # Match any packets
        #    },
        #    'actions': [
        #        {
        #            'type': 'OUTPUT',
        #            'port': ofproto_v1_0.OFPP_NORMAL,
        #            'max_len': ofproto_v1_0.OFPCML_MAX,
        #        },
        #    ]
        #}
        # L2スイッチにする．
        # for datapath in self.datapathes:
        #     ofctl_v1_0.mod_flow_entry(
        #         datapath,
        #         flow,
        #         ofproto_v1_0.OFPFC_ADD,
        #     )

    def set_flow(self, js):
        """ it is called in sr."""
        self.log.info(self.set_flow.__doc__)
        proto = None
        op = None
        for datapath in self.datapathes:
            parser = datapath.ofproto_parser
            proto = datapath.ofproto
            match = parser.OFPMatch(dl_src=js.get('mac1'))
            actions = [     
                #op.OFPActionSetField(dl_dst = js.get('mac2'),),
                parser.OFPActionSetDlSrc('02:00:00:00:00:01'),#haddr_to_bin(js.get('mac2'))),
                parser.OFPActionSetDlDst(js.get('mac2')),#haddr_to_bin(js.get('mac2'))),
                #op.OFPActionSetField(nw_dst = '10.0.0.1'),
                parser.OFPActionSetNwSrc('10.0.0.100'),# ipv4_to_int('10.0.0.1')),
                parser.OFPActionSetNwDst('10.0.0.1'),# ipv4_to_int('10.0.0.1')),
                parser.OFPActionSetTpDst(4000),
                parser.OFPActionOutput(proto.OFPP_IN_PORT)#, ofproto.OFP_NO_BUFFER)#proto.OFPP_NORMAL,3 ,proto.OFP_NO_BUFFER)
            ]
        self.add_flow(datapath, 10, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        proto = datapath.ofproto
        parser = datapath.ofproto_parser
        command = proto.OFPFC_ADD
        cookie = 0
        # inst = []#[parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, actions=actions, command=command, cookie=cookie)#instAructions=inst)
        datapath.send_msg(mod)

class Rest(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(Rest, self).__init__(req, link, data, **config)
        self.sample = data[sample]

    @route('sr', '/api/sr', methods=['POST'])
    def sr(self, req, **kwargs):
        js = literal_eval(req.body)
        self.sample.set_flow(js)

if __name__ == '__main__':
    import sys
    sys.argv.append(__name__)
    sys.argv.append('--verbose')
    from ryu.cmd import manager
    manager.main()

