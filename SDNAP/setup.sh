#!/bin/bash


ovs-vsctl set-controller ovs-br tcp:192.168.52.5:6633
ip link add veth1 type veth peer name veth2
ip link set veth1 up
ip link set veth2 up
brctl addif br1 veth1
ovs-vsctl add-port ovs-br veth2
ip netns add h1
ip netns add h2
ip netns add h3
ip link add veth3 type veth peer name h1-veth addr 02:00:00:00:00:01
ip link add veth4 type veth peer name h2-veth addr 02:00:00:00:00:02
ip link add veth5 type veth peer name h3-veth addr 02:00:00:00:00:03
ip link set h1-veth netns h1
ip link set h2-veth netns h2
ip link set h3-veth netns h3
ip link set veth3 up
ip link set veth4 up
ip link set veth5 up
ip netns exec h1 ip link set h1-veth up
ip netns exec h2 ip link set h2-veth up
ip netns exec h3 ip link set h3-veth up
ovs-vsctl add-port ovs-br veth3
ovs-vsctl add-port ovs-br veth4
ovs-vsctl add-port ovs-br veth5
ip netns exec h1 ip addr add 10.0.0.100/24 dev h1-veth
ip netns exec h2 ip addr add 10.0.0.101/24 dev h2-veth
ip netns exec h3 ip addr add 10.0.0.102/24 dev h3-veth
#ovs-ofctl add-flow ovs-br 'arp,dl_src=02:00:00:00:00:01,actions=Normal'
#ovs-ofctl add-flow ovs-br 'arp,dl_dst=02:00:00:00:00:01,actions=Normal'
