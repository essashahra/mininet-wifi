#!/usr/bin/python

'Setting mechanism to optimize the use of APs'

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8')
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.5/8')
    sta5 = net.addStation('sta5', mac='00:00:00:00:00:06', ip='10.0.0.6/8')
    sta6 = net.addStation('sta6', mac='00:00:00:00:00:07', ip='10.0.0.7/8')
    sta7 = net.addStation('sta7', mac='00:00:00:00:00:08', ip='10.0.0.8/8')
    sta8 = net.addStation('sta8', mac='00:00:00:00:00:09', ip='10.0.0.9/8')
    sta9 = net.addStation('sta9', mac='00:00:00:00:00:10', ip='10.0.0.10/8')
    sta10 = net.addStation('sta10', mac='00:00:00:00:00:11', ip='10.0.0.11/8')
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='50,50,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6', position='70,50,0', range=30)  # range: set the AP range
    ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', mode='g', channel='11', position='90,50,0')
    c1 = net.addController('c1', controller=Controller)

    net.propagationModel("logDistancePropagationLossModel", exp=5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)

    """plotting graph"""
    net.plotGraph(max_x=120, max_y=120)

    """association control"""
    net.associationControl('ssf')

    """Seed"""
    net.seed(1)

    """ *** Available models:
                RandomWalk, TruncatedLevyWalk, RandomDirection, RandomWayPoint, GaussMarkov
    *** Association Control (AC) - mechanism that optimizes the use of the APs:
                llf (Least-Loaded-First)
                ssf (Strongest-Signal-First)"""
    net.startMobility(time=0, model='RandomWayPoint', max_x=120, max_y=120, min_v=0.3, max_v=0.5)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
