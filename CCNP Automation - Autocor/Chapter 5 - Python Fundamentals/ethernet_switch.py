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

interfaces = {
    "Ethernet0/1": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    },
    "Ethernet0/2": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    },
    "Ethernet0/3": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    },
    "Ethernet0/4": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    },
    "Ethernet0/5": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    },
    "Ethernet0/6": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    },
    "Ethernet0/7": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    },
    "Ethernet0/8": {
        "in_frames": 0,
        "in_bytes": 0,
        "out_frames": 0,
        "out_bytes": 0
    }
}

mac_table = {}

def forward_frame(dst_mac, egress_port, size):
    print(f"⏩ Frame with destination {dst_mac} forwarding out of {egress_port}")
    interfaces[egress_port]["out_frames"] += 1
    interfaces[egress_port]["out_bytes"] += size

def flood_frame(dst_mac, ingress_port, size):
    print(f"🌊 Flooding to all other ports")
    for egress_port in interface_names:
        if egress_port != ingress_port:
            forward_frame(dst_mac, egress_port, size)

def incoming_frame(src_mac, dst_mac, ingress_port, size):
    print(f"⚠️ Recieved frame on {ingress_port} from {src_mac} to {dst_mac}")
    interfaces[ingress_port]["in_frames"] += 1
    interfaces[ingress_port]["in_bytes"] += size
    mac_table[src_mac] = ingress_port
    if dst_mac in mac_table:
        egress_port = mac_table[dst_mac]
        print(f"🟢 Address {dst_mac} found in Mac tables on {egress_port}")
        forward_frame(dst_mac, egress_port, size)
    elif dst_mac == "FF:FF:FF:FF:FF:FF":
        print(f"🟡 Destionation is broadcast")
        flood_frame(dst_mac, ingress_port, size)
    else:
        print(f"🔴 Adress {dst_mac} NOT found in MAC table")
        flood_frame(dst_mac, ingress_port, size)

def show_interfaces():
    print("\n! show interfaces")
    for intf_name, counters in interfaces.items():
        print(intf_name)
        print(f"  {counters['in_frames']} frames input, {counters['in_bytes']} bytes")
        print(f"  {counters['out_frames']} frames output, {counters['out_bytes']} bytes")

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
        short_name = intf_name[:3] + intf_name[-3:]
        print(f"{mac_addr}    DYNAMIC    {short_name}")


incoming_frame("00:11:22:33:44:55", "DE:AD:BE:EF:00:03", "Ethernet0/1", 64)
incoming_frame("DE:AD:BE:EF:00:03", "00:11:22:33:44:55", "Ethernet0/2", 1500)
incoming_frame("12:34:56:78:9A:04", "FF:FF:FF:FF:FF:FF", "Ethernet0/2", 84)
incoming_frame("C0:FF:EE:00:00:05", "99:88:77:66:55:06", "Ethernet0/4", 860)
incoming_frame("AA:BB:CC:DD:EE:02", "AB:CD:EF:12:34:08", "Ethernet0/1", 766)
incoming_frame("99:88:77:66:55:06", "02:42:AC:11:00:07", "Ethernet0/5", 901)
incoming_frame("02:42:AC:11:00:07", "FF:FF:FF:FF:FF:FF", "Ethernet0/7", 108)
incoming_frame("AB:CD:EF:12:34:08", "66:77:88:99:AA:01", "Ethernet0/8", 64)
incoming_frame("00:11:22:33:44:55", "C0:FF:EE:00:00:05", "Ethernet0/1", 64)
incoming_frame("66:77:88:99:AA:01", "12:34:56:78:9A:04", "Ethernet0/1", 1500)
incoming_frame("DE:AD:BE:EF:00:03", "AB:CD:EF:12:34:08", "Ethernet0/2", 1496)
incoming_frame("12:34:56:78:9A:04", "C0:FF:EE:00:00:05", "Ethernet0/2", 1360)
incoming_frame("C0:FF:EE:00:00:05", "FF:FF:FF:FF:FF:FF", "Ethernet0/4", 64)
incoming_frame("99:88:77:66:55:06", "00:11:22:33:44:55", "Ethernet0/5", 576)
incoming_frame("02:42:AC:11:00:07", "DE:AD:BE:EF:00:03", "Ethernet0/7", 576)
incoming_frame("AB:CD:EF:12:34:08", "FF:FF:FF:FF:FF:FF", "Ethernet0/8", 256)
incoming_frame("00:11:22:33:44:55", "99:88:77:66:55:06", "Ethernet0/1", 128)
incoming_frame("66:77:88:99:AA:01", "DE:AD:BE:EF:00:03", "Ethernet0/1", 168)
incoming_frame("AA:BB:CC:DD:EE:02", "C0:FF:EE:00:00:05", "Ethernet0/1", 148)
incoming_frame("AA:BB:CC:DD:EE:02", "FF:FF:FF:FF:FF:FF", "Ethernet0/1", 64)
incoming_frame("DE:AD:BE:EF:00:03", "00:11:22:33:44:55", "Ethernet0/2", 576)
incoming_frame("12:34:56:78:9A:04", "AA:BB:CC:DD:EE:02", "Ethernet0/2", 1500)
incoming_frame("C0:FF:EE:00:00:05", "02:42:AC:11:00:07", "Ethernet0/4", 576)
incoming_frame("99:88:77:66:55:06", "AB:CD:EF:12:34:08", "Ethernet0/5", 1280)
incoming_frame("02:42:AC:11:00:07", "66:77:88:99:AA:01", "Ethernet0/7", 1460)
incoming_frame("66:77:88:99:AA:01", "FF:FF:FF:FF:FF:FF", "Ethernet0/1", 576)
incoming_frame("AB:CD:EF:12:34:08", "12:34:56:78:9A:04", "Ethernet0/8", 820)
incoming_frame("00:11:22:33:44:55", "AB:CD:EF:12:34:08", "Ethernet0/1", 1320)

show_mac_address_table()

#show_interfaces()