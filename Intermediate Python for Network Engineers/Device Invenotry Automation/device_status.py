devices = [
    {
        "Name" : "Router1",
        "Management IP" : "10.10.10.1",
        "Device Type" : "Router",
        "Status" : "Online"
    },
    {
        "Name" : "Router2",
        "Management IP" : "10.10.20.1",
        "Device Type" : "Router",
        "Status" : "Online"
    },
    {
        "Name" : "Switch1",
        "Management IP" : "10.10.10.11",
        "Device Type" : "Switch",
        "Status" : "Online"
    },
    {
        "Name" : "Switch2",
        "Management IP" : "10.10.20.11",
        "Device Type" : "Switch",
        "Status" : "Offline"
    }
]

for device in devices:
    if device["Status"] == "Online":
        print(f"Device Name: {device['Name']}")
        print(f"Management IP: {device['Management IP']}")
    elif device['Status'] == "Offline":
        print(f"Skipping {device['Name']} becasue device is offline")
    else:
        print("Could not find device status")