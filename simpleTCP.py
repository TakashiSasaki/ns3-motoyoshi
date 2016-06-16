import ns
from ns.core import CommandLine, StringValue, UintegerValue, Seconds, Simulator
from ns.network import NodeContainer, DropTailQueue, NetDeviceContainer, Ipv4Address, Ipv4Mask, AddressValue, InetSocketAddress, Address, ApplicationContainer
from ns.internet import InternetStackHelper, Ipv4AddressHelper, Ipv4GlobalRoutingHelper, Ipv4InterfaceContainer, TcpSocketFactory
from ns.point_to_point import PointToPointHelper
from ns.applications import BulkSendHelper, PacketSinkHelper
import ns.visualizer
import sys

commandLine = CommandLine()
commandLine.Parse(sys.argv)

internetStackHelper = InternetStackHelper()

# create NetTopology
net1Nodes = NodeContainer()
net1Nodes.Create(2)
print(net1Nodes)

net2Nodes = NodeContainer()
net2Nodes.Add(net1Nodes.Get(1))
net2Nodes.Create(1)
print(net2Nodes)

net3Nodes = NodeContainer()
net3Nodes.Add(net1Nodes.Get(1))
net3Nodes.Create(1)
print(net3Nodes)

# source to center link

pointToPointHelperSourceToCenter = PointToPointHelper()
pointToPointHelperSourceToCenter.SetDeviceAttribute("DataRate", StringValue("5Mbps"))
pointToPointHelperSourceToCenter.SetChannelAttribute("Delay", StringValue("2ms"))

pointToPointHelperSourceToCenter.SetQueue("ns3::DropTailQueue")

devices1 = NetDeviceContainer()
devices1 = pointToPointHelperSourceToCenter.Install(net1Nodes)

devices2 = NetDeviceContainer()
devices2 = pointToPointHelperSourceToCenter.Install(net2Nodes)

# bottleneck link

pointToPointHelperBottleneck = PointToPointHelper()
pointToPointHelperBottleneck.SetDeviceAttribute("DataRate", StringValue("800Kbps"))
pointToPointHelperBottleneck.SetChannelAttribute("Delay", StringValue("5ms"))
pointToPointHelperBottleneck.SetQueue("ns3::DropTailQueue")

devices3 = NetDeviceContainer()
devices3 = pointToPointHelperBottleneck.Install(net3Nodes)

internetStackHelper.InstallAll()

ipv4AddressHelper1 = Ipv4AddressHelper()
ipv4AddressHelper1.SetBase(Ipv4Address("10.1.0.0"), Ipv4Mask("255.255.255.0"), Ipv4Address("0.0.0.1"))
ipv4InterfaceContainer1 = Ipv4InterfaceContainer()
ipv4InterfaceContainer1 = ipv4AddressHelper1.Assign(devices1)

ipv4AddressHelper2 = Ipv4AddressHelper()
ipv4AddressHelper2.SetBase(Ipv4Address("10.2.0.0"), Ipv4Mask("255.255.255.0"), Ipv4Address("0.0.0.1"))
ipv4InterfaceContainer2 = Ipv4InterfaceContainer()
ipv4InterfaceContainer2 = ipv4AddressHelper2.Assign(devices2)

ipv4AddressHelper3 = Ipv4AddressHelper()
ipv4AddressHelper3.SetBase(Ipv4Address("10.3.0.0"), Ipv4Mask("255.255.255.0"), Ipv4Address("0.0.0.1"))
ipv4InterfaceContainer3 = Ipv4InterfaceContainer()
ipv4InterfaceContainer3 = ipv4AddressHelper3.Assign(devices3)

Ipv4GlobalRoutingHelper.PopulateRoutingTables()

# remote

remoteAddress = AddressValue(InetSocketAddress(ipv4InterfaceContainer3.GetAddress(1, 0), 50000))
#remoteAddress(InetSocketAddress(ipv4InterfaceContainer3.GetAddress(1, 0), 50000))

ftp = BulkSendHelper("ns3::TcpSocketFactory", Address())

#ftp max 5MB
ftp.SetAttribute("Remote", remoteAddress)
ftp.SetAttribute("MaxBytes", UintegerValue(5242880))

sourceApp1 = ApplicationContainer()
sourceApp1 = ftp.Install(net1Nodes.Get(0))

sourceApp1.Start(Seconds(2.0))
sourceApp1.Stop(Seconds(4.0))

sourceApp2 = ApplicationContainer()
sourceApp2 = ftp.Install(net2Nodes.Get(1))

sourceApp2.Start(Seconds(2.0))
sourceApp2.Stop(Seconds(4.0))

# sink

sinkAddress = Address(InetSocketAddress(Ipv4Address.GetAny(), 50000))
sinkHelper = PacketSinkHelper("ns3::TcpSocketFactory", sinkAddress)

sinkApps = ApplicationContainer()
sinkApps = sinkHelper.Install(net3Nodes.Get(1))

sinkApps.Start(Seconds(1.0))
sinkApps.Stop(Seconds(20.0))

pointToPointHelperBottleneck.EnablePcapAll("SiTCP")

Simulator.Run()
Simulator.Destroy()
