#!/usr/bin/python
'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2
Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
course work by: Joe Ryan - July 14, 2015
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        self.fanout = fanout
         
        coreSwitch = self.addSwitch('c1')
        # aggregation layer
        agg = 0
        edge = 0
        for i in range(1, fanout+1):
            aggSwitch = self.addSwitch("a%d" % i)
            for j in range(agg*fanout + 1, agg * fanout + 1 + fanout):
                edgeSwitch = self.addSwitch("e%d" % j)
                for k in range(edge * fanout + 1, edge * fanout + fanout +1):
                    host = self.addHost("h%d" % k)
                    self.addLink(host, edgeSwitch, bw=linkopts3['bw'], delay=linkopts3['delay'])
                self.addLink(edgeSwitch, aggSwitch, bw=linkopts2['bw'], delay=linkopts2['delay'])
                edge += 1
            self.addLink(aggSwitch, coreSwitch, bw=linkopts1['bw'], delay=linkopts1['delay'])
            agg += 1
            
                    
        
                    
topos = { 'custom': ( lambda: CustomTopo() ) }

def simpleTest():
   "Create and test a simple network"
   corelink = dict(bw=1000, delay='10ms')
   agglink = dict(bw=100, delay='20ms')
   edgelink = dict(bw=10, delay='50ms')
   
   topo = CustomTopo(linkopts1=corelink, linkopts2=agglink, linkopts3=edgelink, fanout=3)
   net = Mininet(topo=topo, link=TCLink)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   net.stop()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()