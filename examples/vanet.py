#!/usr/bin/python

'Simple idea around Vehicular Ad Hoc Networks - VANETs'

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import os
import random

def topology():

    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    car = []
    stas = []
    for x in range(0, 10):
        car.append(x)
        stas.append(x)
    for x in range(0, 10):
        min = random.randint(1, 10)
        max = random.randint(11, 30)
        car[x] = net.addCar('car%s' % (x + 1), wlans=1, ip='10.0.0.%s/8' % (x + 1), min_speed=min, max_speed=max)

    rsu11 = net.addAccessPoint('RSU11', ssid='RSU11', mode='g', channel='1', range=50)
    rsu12 = net.addAccessPoint('RSU12', ssid='RSU12', mode='g', channel='6', range=50)
    rsu13 = net.addAccessPoint('RSU13', ssid='RSU13', mode='g', channel='11', range=50)
    rsu14 = net.addAccessPoint('RSU14', ssid='RSU14', mode='g', channel='11', range=50)
    c1 = net.addController('c1', controller=Controller)

    print "*** Configuring Propagation Model"
    net.propagationModel("logDistancePropagationLossModel", exp=4)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(rsu11, rsu12)
    net.addLink(rsu11, rsu13)
    net.addLink(rsu11, rsu14)

    """plotting graph"""
    net.plotGraph(max_x=500, max_y=500)

    """Number of Roads"""
    net.roads(10)

    """Start Mobility"""
    net.startMobility(time=0)

    print "*** Starting network"
    net.build()
    c1.start()
    rsu11.start([c1])
    rsu12.start([c1])
    rsu13.start([c1])
    rsu14.start([c1])

    i = 201
    for sw in net.carsSW:
        sw.start([c1])
        os.system('ip addr add 10.0.0.%s dev %s' % (i, sw))
        i += 1

    i = 1
    j = 2
    k = 1
    for c in car:
        c.setIP('192.168.0.%s/24' % k, intf='%s-wlan0' % c)
        c.setIP('192.168.1.%s/24' % i, intf='%s-eth0' % c)
        c.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2
        k += 1

    i = 1
    j = 2
    for v in net.carsSTA:
        v.setIP('192.168.1.%s/24' % j, intf='%s-eth0' % v)
        v.setIP('10.0.0.%s/24' % i, intf='%s-mp0' % v)
        v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for v1 in net.carsSTA:
        i = 1
        j = 1
        for v2 in net.carsSTA:
            if v1 != v2:
                v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
