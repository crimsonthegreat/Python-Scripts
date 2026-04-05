from netmiko import ConnectHandler

device_info = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'cisco',
    'password': '1234qwer',
    'secret': '1234qwer'
}

net_connect = ConnectHandler(**device_info)
print(f"Established the SSH connections to device {device_info['host']}")

net_connect.enable()
print("The privileged mode on the device is active")

config_commands = [
    'interface loopback100',
    'ip address 10.10.10.10 255.255.255.255',
    'description test interface'
]
config_output = net_connect.send_config_set(config_commands)
print(f"Configuration Output:\n{config_output}")

output = net_connect.send_config_from_file('loopback101.cfg')
print(output)

output = net_connect.send_command('show ip interface brief')
print(f"Show Command Output:\n{output}")