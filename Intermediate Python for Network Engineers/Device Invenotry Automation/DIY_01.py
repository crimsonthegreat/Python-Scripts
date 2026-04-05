device_name = "Switch1"
ip_address = "192.168.100.1"
port_count = 48
is_active = True

print(f"Device Name: {device_name}")
print(f"IP address: {ip_address}")
print(f"Port count: {port_count}")
print(f"Is Active: {is_active}")


print("\nData Types:")
print(f"Type of device_name: {type(device_name)}")
print(f"Type of ip_address: {type(ip_address)}")
print(f"Type of port_count: {type(port_count)}")
print(f"Type of is_active: {type(is_active)}")

is_active = False
print(F"\nUpdated Is Active: {is_active}")