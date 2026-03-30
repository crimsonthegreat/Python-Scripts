interface_names = [
    "Ethernet0/1",
    "Ethernet0/2",
    "Ethernet0/3",
    "Ethernet0/4",
    "Ethernet0/5",
    "Ethernet0/6",
    "Ethernet0/7",
    "Ethernet0/8"
]

mac_table = {}

def forward_frame(dst_mac, egress_port):
    print(f"⏩ Frame with destination {dst_mac} forwarding out of {egress_port}")

def flood_frame(dst_mac, ingress_port):
    print(f"🌊 Flooding to all other ports")
    for egress_port in interface_names:
        if egress_port != ingress_port:
            forward_frame(dst_mac, egress_port)

def incoming_frame(src_mac, dst_mac, ingress_port):
    print(f"⚠️ Recieved frame on {ingress_port} from {src_mac} to {dst_mac}")
    mac_table[src_mac] = ingress_port
    if dst_mac in mac_table:
        egress_port = mac_table[dst_mac]
        print(f"🟢 Address {dst_mac} found in Mac tables on {egress_port}")
        forward_frame(dst_mac, egress_port)
    elif dst_mac == "FF:FF:FF:FF:FF:FF":
        print(f"🟡 Destionation is broadcast")
        flood_frame(dst_mac, ingress_port)
    else:
        print(f"🔴 Adress {dst_mac} NOT found in MAC table")
        flood_frame(dst_mac, ingress_port)


def show_mac_address_table():
    sh_mac_addr_banner = """
! show mac address-table

    Mac Address Table
-----------------------------------

Mac Address          Type       Ports
-----------          -------    -----
"""
    print(sh_mac_addr_banner)
    for mac_addr, intf_name in sorted(mac_table.items()):
        print(f"{mac_addr}    DYNAMIC    {intf_name}")

incoming_frame("00:11:22:33:44:55", "DE:AD:BE:EF:00:03", "Ethernet0/1")
incoming_frame("DE:AD:BE:EF:00:03", "00:11:22:33:44:55", "Ethernet0/2")
incoming_frame("12:34:56:78:9A:04", "FF:FF:FF:FF:FF:FF", "Ethernet0/2")
incoming_frame("C0:FF:EE:00:00:05", "99:88:77:66:55:06", "Ethernet0/4")
incoming_frame("AA:BB:CC:DD:EE:02", "AB:CD:EF:12:34:08", "Ethernet0/1")
incoming_frame("99:88:77:66:55:06", "02:42:AC:11:00:07", "Ethernet0/5")
incoming_frame("02:42:AC:11:00:07", "FF:FF:FF:FF:FF:FF", "Ethernet0/7")
incoming_frame("AB:CD:EF:12:34:08", "66:77:88:99:AA:01", "Ethernet0/8")
incoming_frame("00:11:22:33:44:55", "C0:FF:EE:00:00:05", "Ethernet0/1")
incoming_frame("66:77:88:99:AA:01", "12:34:56:78:9A:04", "Ethernet0/1")
incoming_frame("DE:AD:BE:EF:00:03", "AB:CD:EF:12:34:08", "Ethernet0/2")
incoming_frame("12:34:56:78:9A:04", "C0:FF:EE:00:00:05", "Ethernet0/2")
incoming_frame("C0:FF:EE:00:00:05", "FF:FF:FF:FF:FF:FF", "Ethernet0/4")
incoming_frame("99:88:77:66:55:06", "00:11:22:33:44:55", "Ethernet0/5")
incoming_frame("02:42:AC:11:00:07", "DE:AD:BE:EF:00:03", "Ethernet0/7")
incoming_frame("AB:CD:EF:12:34:08", "FF:FF:FF:FF:FF:FF", "Ethernet0/8")
incoming_frame("00:11:22:33:44:55", "99:88:77:66:55:06", "Ethernet0/1")
incoming_frame("66:77:88:99:AA:01", "DE:AD:BE:EF:00:03", "Ethernet0/1")
incoming_frame("AA:BB:CC:DD:EE:02", "C0:FF:EE:00:00:05", "Ethernet0/1")
incoming_frame("AA:BB:CC:DD:EE:02", "FF:FF:FF:FF:FF:FF", "Ethernet0/1")
incoming_frame("DE:AD:BE:EF:00:03", "00:11:22:33:44:55", "Ethernet0/2")
incoming_frame("12:34:56:78:9A:04", "AA:BB:CC:DD:EE:02", "Ethernet0/2")
incoming_frame("C0:FF:EE:00:00:05", "02:42:AC:11:00:07", "Ethernet0/4")
incoming_frame("99:88:77:66:55:06", "AB:CD:EF:12:34:08", "Ethernet0/5")
incoming_frame("02:42:AC:11:00:07", "66:77:88:99:AA:01", "Ethernet0/7")
incoming_frame("66:77:88:99:AA:01", "FF:FF:FF:FF:FF:FF", "Ethernet0/1")
incoming_frame("AB:CD:EF:12:34:08", "12:34:56:78:9A:04", "Ethernet0/8")
incoming_frame("00:11:22:33:44:55", "AB:CD:EF:12:34:08", "Ethernet0/1")

show_mac_address_table()