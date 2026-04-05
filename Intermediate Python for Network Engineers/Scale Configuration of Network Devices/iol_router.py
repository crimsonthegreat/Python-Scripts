from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import re

env = Environment(loader=FileSystemLoader('.'))

template = env.get_template('iol_router.j2')

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'cisco',
        'password': '1234qwer',
        'secret': '1234qwer'
    },
    {
        'device_type': 'cisco_ios',
        'host': '192.168.1.2',
        'username': 'cisco',
        'password': '1234qwer',
        'secret': '1234qwer'
    }
]

for device in devices:
    rendered_config = template.render(
        X=devices.index(device) + 1, 
        loopback100="10.10.10." + str(devices.index(device) + 1)
        )

    net_connect = ConnectHandler(**device)

    print(f"Established SSH connections to device {device['host']}")
    
    net_connect.enable()
    print(f"Privileged mode on device {device['host']} is active")

    config_commands = rendered_config.splitlines()
    output = net_connect.send_config_set(config_commands)
    print(f"Configuration Output for device {device['host']}:\n{output}")

    print(f"Device {device['host']} configuration completed.\n")

    output = net_connect.send_command('show interface Ethernet0/1')
    if 'Ethernet0/1 is up' in output:
        print("The interface Ethernet0/1 is currently in the UP state")
    else:
        print("The interface Ethernet0/1 is currently in the DOWN state")

    output = net_connect.send_command("show version")
    pattern = r"Version\s+([\d\.]+[^\s!=,]*)"

    match = re.search(pattern, output)
    if match:
        print(f"version found: {match.group(1)}\n")
    else:
        print("No Version found\n")

