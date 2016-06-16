import ns
from ns.point_to_point import PointToPointHelper
from ns.point_to_point_layout import PointToPointDumbbellHelper
from ns.core import Simulator, Seconds, UintegerValue, TimeValue, CommandLine, MilliSeconds, StringValue
from ns.internet import InternetStackHelper
from ns.internet import Ipv4AddressHelper, Ipv4GlobalRoutingHelper
from ns.network import Ipv4Address, Ipv4Mask, Node
from ns.applications import UdpEchoServerHelper, UdpEchoClientHelper
import ns.visualizer
import sys

command_line = CommandLine()
command_line.Parse(sys.argv)

point_to_point_helper = PointToPointHelper()
point_to_point_helper.SetDeviceAttribute("DataRate", StringValue("5Mbps"))
point_to_point_helper.SetChannelAttribute("Delay", StringValue("2ms"))
point_to_point_helper_bottleneck = PointToPointHelper()
point_to_point_helper_bottleneck.SetDeviceAttribute("DataRate", StringValue("5Mbps"))
point_to_point_helper_bottleneck.SetChannelAttribute("Delay", StringValue("2ms"))

point_to_point_dumbbell_helper = PointToPointDumbbellHelper(2, point_to_point_helper, 2, point_to_point_helper, point_to_point_helper_bottleneck)

internet_stack_helper = InternetStackHelper()
#internet_stack_helper.EnablePcapAll("dumbbell", False)
point_to_point_dumbbell_helper.InstallStack(internet_stack_helper)


# left leaf
ipv4_address_helper1 = Ipv4AddressHelper()
ipv4_address_helper1.SetBase(Ipv4Address("10.1.1.0"), Ipv4Mask("255.255.255.0"))

# right leaf
ipv4_address_helper2 = Ipv4AddressHelper()
ipv4_address_helper2.SetBase(Ipv4Address("10.2.1.0"), Ipv4Mask("255.255.255.0"))

# bottlenecl
ipv4_address_helper3 = Ipv4AddressHelper()
ipv4_address_helper3.SetBase(Ipv4Address("10.3.1.0"), Ipv4Mask("255.255.255.0"))

point_to_point_dumbbell_helper.AssignIpv4Addresses(ipv4_address_helper1, ipv4_address_helper2, ipv4_address_helper3)

#ipv4_global_routing_helper = Ipv4GlobalRoutingHelper()
#ipv4_global_routing_helper.PolulateRoutingTables()
Ipv4GlobalRoutingHelper.PopulateRoutingTables()

left_node_1 = point_to_point_dumbbell_helper.GetLeft(0)
left_node_1_address = left_node_1.GetDevice(1).GetAddress()
print (left_node_1_address)
right_node_1 = point_to_point_dumbbell_helper.GetRight(0)
right_node_1_address = right_node_1.GetDevice(1).GetAddress()
print (right_node_1_address)

left_node_2 = point_to_point_dumbbell_helper.GetLeft(1)
left_node_2_address = left_node_2.GetDevice(1).GetAddress()
print (left_node_2_address)
right_node_2 = point_to_point_dumbbell_helper.GetRight(1)
right_node_2_address = right_node_2.GetDevice(1).GetAddress()
print (right_node_2_address)

udp_echo_server_helper = UdpEchoServerHelper(50000)

server = udp_echo_server_helper.Install(left_node_1)
server.Start(Seconds(1.0))
server.Stop(Seconds(10.0))

udp_echo_client_helper = UdpEchoClientHelper(Ipv4Address("10.1.1.1"), 50000)
udp_echo_client_helper.SetAttribute("MaxPackets", UintegerValue(1000))
#udp_echo_client_helper.SetAttribute("Interval", TimeValue(Seconds(1.0)))
#udp_echo_client_helper.SetAttribute("Interval", TimeValue(Seconds(0.1)))
udp_echo_client_helper.SetAttribute("Interval", TimeValue(Seconds(0.01)))
udp_echo_client_helper.SetAttribute("PacketSize", UintegerValue(1024))

client_1 = udp_echo_client_helper.Install(right_node_1)
client_1.Start(Seconds(2.0))
client_1.Stop(Seconds(9.0))

client_2 = udp_echo_client_helper.Install(right_node_2)
client_2.Start(Seconds(2.0))
client_2.Stop(Seconds(9.0))

client_3 = udp_echo_client_helper.Install(left_node_2)
client_3.Start(Seconds(2.0))
client_3.Stop(Seconds(9.0))

point_to_point_helper.EnablePcapAll("dumbbell")
#PointToPointHelper.EnablePcapHelper("dumbbell")

Simulator.Run()
Simulator.Destroy()
