#!/usr/bin/python

"""
Replaying Bandwidth
"""

from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.wifiReplaying import replayingBandwidth

def topology():

    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8' )
    ap1 = net.addAccessPoint( 'ap1', ssid= 'new-ssid', mode= 'g', channel= '1', position='50,50,0' )
    c1 = net.addController( 'c1', controller=Controller )

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** adding Link"
    net.addLink(sta1, ap1)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )

    """uncomment to plot graph"""
    net.plotGraph(max_x=100, max_y=100)

    getTrace(sta1, 'examples/replaying/replayingBandwidth/throughputData.dat')

    replayingBandwidth(net)

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

def getTrace(sta, file):

    file = open(file, 'r')
    raw_data = file.readlines()
    file.close()

    sta.time = []
    sta.throughput = []

    for data in raw_data:
        line = data.split()
        sta.time.append(float(line[0])) #First Column = Time
        sta.throughput.append(float(line[1])) #Second Column = Throughput

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
