#!/usr/bin/env python

"""Sample file for VANET

***Requirements***:
Kernel version: 5.8+ (due to the 802.11p support)
sumo 1.5.0 or higher
sumo-gui

Please consider reading https://mininet-wifi.github.io/80211p/ for 802.11p support
"""

from mininet.node import RemoteController, OVSKernelSwitch, Controller
from mn_wifi.node import OVSKernelAP
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference
from time import sleep

def topology():
	cars = 10
	"Create a network."
	net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
	info("*** Creating nodes\n")

	for id in range(0, cars):
		net.addCar('car%s' % (id+1),  wlans=2, bgscan_threshold=-45, s_inverval=5, l_interval=10, bgscan_module="simple")

	kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'failMode': 'standalone'}

	#s0 = net.addSwitch('s0', cls=OVSKernelSwitch)

	rsu1 = net.addAccessPoint('rsu1', cls=OVSKernelAP, mac='00:00:00:11:00:01', channel='5', position='2168,228,0', **kwargs)
	rsu3 = net.addAccessPoint('rsu3', cls=OVSKernelAP, mac='00:00:00:11:00:03', channel='5', position='1903,364,0', **kwargs)
	rsu4 = net.addAccessPoint('rsu4', cls=OVSKernelAP, mac='00:00:00:11:00:04', channel='5', position='1655,490,0', **kwargs)
	rsu2 = net.addAccessPoint('rsu2', cls=OVSKernelAP, mac='00:00:00:11:00:02', channel='5', position='1487,621,0', **kwargs)
	rsu5 = net.addAccessPoint('rsu5', cls=OVSKernelAP, mac='00:00:00:11:00:05', channel='5', position='1258,717,0', **kwargs)
	rsu6 = net.addAccessPoint('rsu6', cls=OVSKernelAP, mac='00:00:00:11:00:06', channel='5', position='902,810,0', **kwargs)
	rsu7 = net.addAccessPoint('rsu7', cls=OVSKernelAP, mac='00:00:00:11:00:07', channel='5', position='660,892,0', **kwargs)

	c0 = net.addController(name='c0',
	                   controller=RemoteController,
	                   protocol='tcp',
	                   port=6653)

	info("*** Configuring Propagation Model\n")
	net.setPropagationModel(model="logDistance", exp=2.8)

	info("*** Configuring nodes\n")
	net.configureWifiNodes()
	
	net.addLink(rsu1, rsu3)
	net.addLink(rsu3, rsu4)
	net.addLink(rsu4, rsu2)
	net.addLink(rsu2, rsu5)
	net.addLink(rsu5, rsu6)
	net.addLink(rsu6, rsu7)
	for car in net.cars:
		net.addLink(car, intf='%s-wlan1' % car, cls=mesh, ssid='mesh-ssid')

	net.useExternalProgram(program=sumo, port=8813,
	                   config_file='tcc_sim.sumocfg', clients=1, extra_params=["--start --delay 1000"])

	info("*** Starting network\n")
	net.build()
	c0.start()
	for rsu in net.aps:
		rsu.start([c0])

	for id, car in enumerate(net.cars):
		car.setIP('192.168.0.{}/24'.format(id+1), intf='{}'.format(car.wintfs[0].name))
		car.setIP('192.168.1.{}/24'.format(id+1), intf='{}'.format(car.wintfs[1].name))
		car.cmdPrint('./auto-up.sh &')
		car.cmdPrint('iperf3 -s &')

	nodes = net.cars + net.aps
	net.telemetry(nodes=nodes, data_type='position',
	          min_x=-500, min_y=-500,
	          max_x=2500, max_y=2500)

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topology()
