#List of network devices
device_inventory = [
    {
        "device_name" : "Switch1",
        "ip_address" : "192.168.100.1",
        "port_count" : 48,
        "is_active" : True
    },
    {
        "device_name" : "Router1",
        "ip_address" : "192.168.100.254",
        "port_count" : 8,
        "is_active" : True
    }
]

print(f"List of network devices: {device_inventory}")

print(f"Setting is active on {device_inventory[1]["device_name"]} to False")

#Set is_active to False for second device in the list
device_inventory[1]["is_active"] = False
print(f"Verify {device_inventory[1]["device_name"]} is set correctly.  Value should be False:")

#Validate the value is set to False
if device_inventory[1]["is_active"] == True:
    print(f"\nThe value for {device_inventory[1]['is_active']} is not set correctly")
else:
    print(f"The value is set correctly to {device_inventory[1]["is_active"]}")

print(f"Adding a new device to the list.")
device_inventory.append(
    {
        "device_name" : "Switch2",
        "ip_address" : "192.168.100.10",
        "port_count" : 24,
        "is_active" : True
    }
)

print(f"\nNew list of devices: {device_inventory}")

#Delete the second device in the list
del device_inventory[1]
print(f"\nUpdated list of devices: {device_inventory}")

#Use remove to specify the device to remove from the list
device_to_remove = {
        "device_name" : "Switch2",
        "ip_address" : "192.168.100.10",
        "port_count" : 24,
        "is_active" : True
    }

print(f"\nRemoving {device_to_remove['device_name']} for the list.")
device_inventory.remove(device_to_remove)
print(f"\nFinal list of devices: {device_inventory}")