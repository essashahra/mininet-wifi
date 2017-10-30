#!/usr/bin/python

'Setting the position of nodes'

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():

    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', position='10,20,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', position='10,30,0')
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', position='15,30,0')
    c1 = net.addController('c1', controller=Controller)
    h1 = net.addHost ('h1', ip='10.0.0.3/8')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(ap1, h1)

    """plotting graph"""
    net.plotGraph(max_x=100, max_y=100)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

