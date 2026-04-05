r1_hosts = {
    '10.10.10.2': '00:11:22:33:44:55',
    '10.10.10.3': 'C0:FF:EE:00:00:05',
    '10.10.10.4': 'AA:BB:CC:DD:EE:FF',
    '10.10.10.5': 'DE:AD:BE:EF:00:04',
    '10.10.10.6': '99:88:77:66:55:44',
    '10.10.10.7': '12:34:56:78:9A:BC'
}

my_hosts = {
    '10.10.10.2': '00:11:22:33:44:55',
    '10.10.10.3': 'C0:FF:EE:00:00:05'
}

print("Welcome to PythonArpCache!")
while not r1_hosts.items() <= my_hosts.items():
    ip_addr = input("Which IP address to look up? ")

    mac_addr = my_hosts.get(ip_addr)

    if mac_addr:
        print(f"The host IP address {ip_addr} maps to Mac address {mac_addr}")
    else:
        print(f"The host IP address {ip_addr} is not found")
        print("Checking Router 1 for ARP ...")
        r1_mac_addr = r1_hosts.get(ip_addr)
        if r1_mac_addr:
            my_hosts[ip_addr] = r1_mac_addr
            print(f"ARP record found on Router 1!")
            print(f"The host IP address {ip_addr} maps to Mac address {r1_mac_addr}")

            print("! show ip arp")
            print("Protocol  Hardware Addr      Type  Address")
            for cached_ip, cached_mac in my_hosts.items():
                print(F"Internet  {cached_mac}  ARPA  {cached_ip}")
        else:
            my_hosts[ip_addr] = "Incomplete       "

            print("! show ip arp")
            print("Protocol  Hardware Addr      Type  Address")
            for cached_ip, cached_mac in my_hosts.items():
                print(F"Internet  {cached_mac}  ARPA  {cached_ip}")