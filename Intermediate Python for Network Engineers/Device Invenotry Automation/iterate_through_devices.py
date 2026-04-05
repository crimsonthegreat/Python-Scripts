devices = [
    {
        "Name" : "Router1",
        "Management IP" : "10.10.10.1",
        "Device Type" : "Router"
    },
    {
        "Name" : "Router2",
        "Management IP" : "10.10.20.1",
        "Device Type" : "Router"
    },
    {
        "Name" : "Switch1",
        "Management IP" : "10.10.10.11",
        "Device Type" : "Switch"
    }
]

for device in devices:
    print(f"Device name: {device['Name']}")
    print(f"Management IP: {device['Management IP']}")
    print(f"Device Type: {device['Device Type']}")
    print("")