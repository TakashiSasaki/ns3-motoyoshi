import ns
import sys
import ns.visualizer
from ns.core import CommandLine, StringValue, Seconds, Simulator, TimeValue
from ns.point_to_point import PointToPointHelper
from ns.point_to_point_layout import PointToPointStarHelper
from ns.internet import InternetStackHelper, Ipv4AddressHelper, Ipv4GlobalRoutingHelper
from ns.network import Ipv4Address, Ipv4Mask, Address, ApplicationContainer, AddressValue, InetSocketAddress
from ns.applications import OnOffHelper, PacketSinkHelper

commandLine = CommandLine()
commandLine.Parse(sys.argv)

# Build Star Topology
pointToPointHelper = PointToPointHelper()
pointToPointHelper.SetDeviceAttribute("DataRate", StringValue("5Mbps"))
pointToPointHelper.SetChannelAttribute("Delay", StringValue("2ms"))
pointToPointStarHelper = PointToPointStarHelper(5, pointToPointHelper)

# Install Internet Stack On All Nodes
internetStackHelper = InternetStackHelper()
pointToPointStarHelper.InstallStack(internetStackHelper)

# Assign IP Address
pointToPointStarHelper.AssignIpv4Addresses(Ipv4AddressHelper(Ipv4Address("10.1.1.0"), Ipv4Mask("255.255.255.0")))

# Create A Packet Sink On The Star "Hub" To Recieve Packets
hubLocalAddress = Address(InetSocketAddress(Ipv4Address.GetAny(), 50000))
packetSinkHelper = PacketSinkHelper("ns3::TcpSocketFactory", hubLocalAddress)
hubApp = ApplicationContainer()
hubApp = packetSinkHelper.Install(pointToPointStarHelper.GetHub())
hubApp.Start(Seconds(1.0))
hubApp.Stop(Seconds(10.0))

# Create On-Off Applications To Send TCP To The Hub. One On Each Spoke Node.
onOffHelper = OnOffHelper("ns3::TcpSocketFactory", Address())
onOffHelper.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=1]"))
onOffHelper.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"))

spokeApps = ApplicationContainer()
spokeCount = pointToPointStarHelper.SpokeCount()

for i in range(spokeCount):
	remoteAddress = AddressValue(InetSocketAddress(pointToPointStarHelper.GetHubIpv4Address(i), 50000))
	onOffHelper.SetAttribute("Remote", remoteAddress)
	spokeApps.Add(onOffHelper.Install(pointToPointStarHelper.GetSpokeNode(i)))

spokeApps.Start(Seconds(2.0))
spokeApps.Stop(Seconds(9.0))

Ipv4GlobalRoutingHelper.PopulateRoutingTables()

pointToPointHelper.EnablePcapAll("starX")

Simulator.Run()
Simulator.Destroy()
