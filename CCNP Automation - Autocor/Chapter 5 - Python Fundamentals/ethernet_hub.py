hubports = [
    "Ethernet0/0",
    "Ethernet0/1",
    "Ethernet0/2",
    "Ethernet0/3"
]

boot_message = """
PythonHub is booting ...
Please wait
"""
print(boot_message)

for hubport in hubports:
    print(hubport)

while True:
    try:
        port = input("Generate signal into port: ")
        port_number = int(port)
        if port_number < len(hubports) and port_number >= 0:
            ingress_port = hubports[port_number]
            print("⚡️ Receiving signal on " + ingress_port)
        else:
            print("❌ Invalid entry: " + port)
            break

        for egress_port in hubports:
            if egress_port == ingress_port:
                print("🔴 Not transmitting on port " + egress_port)
            else:
                print("🟢 Transmitting on port " + egress_port)
                
    except ValueError:
        print("❌ You must enter a number!")