#!/bin/bash

ovs-vsctl del-controller ovs-br
brctl delif br1 veth1
ovs-vsctl del-port ovs-br veth2
ovs-vsctl del-port ovs-br veth3
ovs-vsctl del-port ovs-br veth4
ovs-vsctl del-port ovs-br veth5
