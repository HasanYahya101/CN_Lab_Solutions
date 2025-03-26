import ns.core
import ns.network
import ns.internet
import ns.point_to_point
import ns.applications
import ns.netanim


def main():

    # Create 4 Nodes: n0, n1, n2, n3
    nodes = ns.network.NodeContainer()
    nodes.Create(4)  # n0, n1, n2, n3

    # n0 <-> n2 (2 Mbps, 10 ms)
    p2p_2mbps_10ms = ns.point_to_point.PointToPointHelper()
    p2p_2mbps_10ms.SetDeviceAttribute("DataRate", ns.core.StringValue("2Mbps"))
    p2p_2mbps_10ms.SetChannelAttribute("Delay", ns.core.StringValue("10ms"))
    p2p_2mbps_10ms.SetQueue("ns3::DropTailQueue",
                            "MaxSize", ns.core.StringValue("10p"))

    
    # n2 <-> n3 (1.7 Mbps, 20 ms)
    p2p_1_7mbps_20ms = ns.point_to_point.PointToPointHelper()
    p2p_1_7mbps_20ms.SetDeviceAttribute("DataRate", ns.core.StringValue("1.7Mbps"))
    p2p_1_7mbps_20ms.SetChannelAttribute("Delay", ns.core.StringValue("20ms"))
    p2p_1_7mbps_20ms.SetQueue("ns3::DropTailQueue",
                              "MaxSize", ns.core.StringValue("10p"))

    devices_n0_n2 = p2p_2mbps_10ms.Install(nodes.Get(0), nodes.Get(2))
    devices_n1_n2 = p2p_2mbps_10ms.Install(nodes.Get(1), nodes.Get(2))
    devices_n2_n3 = p2p_1_7mbps_20ms.Install(nodes.Get(2), nodes.Get(3))

    internet = ns.internet.InternetStackHelper()
    internet.Install(nodes)

    ipv4 = ns.internet.Ipv4AddressHelper()

    # n0-n2
    ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    interfaces_n0_n2 = ipv4.Assign(devices_n0_n2)

    # n1-n2
    ipv4.SetBase(ns.network.Ipv4Address("10.1.2.0"), ns.network.Ipv4Mask("255.255.255.0"))
    interfaces_n1_n2 = ipv4.Assign(devices_n1_n2)

    # n2-n3
    ipv4.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0"))
    interfaces_n2_n3 = ipv4.Assign(devices_n2_n3)

    tcp_sink_helper = ns.applications.PacketSinkHelper(
        "ns3::TcpSocketFactory",
        ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 8080)
    )
    tcp_sink_app = tcp_sink_helper.Install(nodes.Get(3))
    tcp_sink_app.Start(ns.core.Seconds(0.0))
    tcp_sink_app.Stop(ns.core.Seconds(5.0))

    bulk_send_helper = ns.applications.BulkSendHelper(
        "ns3::TcpSocketFactory",
        ns.network.InetSocketAddress(interfaces_n2_n3.GetAddress(1), 8080)
    )
    bulk_send_helper.SetAttribute("MaxBytes", ns.core.UintegerValue(0))
    tcp_app = bulk_send_helper.Install(nodes.Get(1))
    tcp_app.Start(ns.core.Seconds(0.5))
    tcp_app.Stop(ns.core.Seconds(4.0))

    udp_sink_helper = ns.applications.PacketSinkHelper(
        "ns3::UdpSocketFactory",
        ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), 8081)
    )
    udp_sink_app = udp_sink_helper.Install(nodes.Get(3))
    udp_sink_app.Start(ns.core.Seconds(0.0))
    udp_sink_app.Stop(ns.core.Seconds(5.0))

    onoff_cbr = ns.applications.OnOffHelper(
        "ns3::UdpSocketFactory",
        ns.network.InetSocketAddress(interfaces_n2_n3.GetAddress(1), 8081)
    )

    onoff_cbr.SetAttribute("DataRate", ns.core.StringValue("800Kbps"))
    onoff_cbr.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

    onoff_cbr.SetAttribute("OnTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=1]"))
    onoff_cbr.SetAttribute("OffTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=0]"))

    cbr_app = onoff_cbr.Install(nodes.Get(0))
    cbr_app.Start(ns.core.Seconds(0.1))
    cbr_app.Stop(ns.core.Seconds(4.5))
    anim = ns.netanim.AnimationInterface("lab08.xml")
    anim.SetConstantPosition(nodes.Get(0), 0.0,  50.0)   # n0
    anim.SetConstantPosition(nodes.Get(1), 0.0, 150.0)   # n1
    anim.SetConstantPosition(nodes.Get(2), 50.0, 100.0)  # n2
    anim.SetConstantPosition(nodes.Get(3), 100.0, 100.0) # n3
    anim.EnablePacketMetadata(True)
    p2p_2mbps_10ms.EnablePcapAll("lab08-p2p2mbps")
    p2p_1_7mbps_20ms.EnablePcapAll("lab08-p2p1.7mbps")
    ns.core.Simulator.Stop(ns.core.Seconds(5.0))
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()

if __name__ == '__main__':
    main()
