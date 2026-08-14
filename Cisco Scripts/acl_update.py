import netmiko
import getpass
import ipaddress
import subprocess

print("*** ACL Update ***")
print("This script can be used to update the ACL on a network device\n")

def connect_info():
    """Function to allow connection to device"""

    ip = input("Please Enter the IP Address: ")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    cisco = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password
    }

    return cisco

def ping_device(ip, count=1, timeout=2):
    """Function to ping a device"""

    cmd = [
        "ping",
        "-c", str(count),
        "-W", str(timeout),
        ip
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=(count * timeout) + 2
        )

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        return False

    except Exception as e:
        print(f"Ping failed: {e}")
        return False

def user_input(prompt):
    """Function for repeated user promptsto continue"""
    
    while True:
        user_input = input(prompt).lower().strip()

        if user_input in ("n", "no"):
            quit()
        elif user_input in ("y","yes"):
            break
        elif user_input == "q":
            quit()
        else:
            print("Please enter y or n to continue!")

def get_acl_type():
    """Function to know which ACL type is being updated"""

    acl_type = ["standard", "extended", "standard named", "extended named"]
    number = 1

    for list in acl_type:
        print(f"\n{number}) {list}:")
        number += 1

    while True:
        select_acl_type = input("\nPlease select an ACL Type [1-4]: ").strip()
        try:
            select_acl_type = int(select_acl_type)

            if select_acl_type == 1 or select_acl_type == 2 or select_acl_type == 3 or select_acl_type == 4:
                selected_acl_type = acl_type[select_acl_type - 1]
                break
            else:
                print("Please enter a number between 1 and 4!")

        except ValueError:
            print("Please enter a number between 1 and 4!")

    print(f"You have selected {selected_acl_type} ACL\n")

    return selected_acl_type
            
def get_acl_name(selected_acl_type):
    """Function to access the specific ACL"""

    while True:
        if selected_acl_type == "standard":
            acl = input("Please Enter the number of the ACL [1-99 or 1300-1999]: ")
            try:
                acl = int(acl)
                if 1 <= acl <= 99 or 1300 <= acl <= 1999:
                    break
                else:
                    print("Please enter a number between 1-99 or 1300-1999")
            except ValueError:
                print("Please enter a number between 1-99 or 1300-1999")
        elif selected_acl_type == "extended":
            acl = input("Please Enter the number of the ACL [100-199 or 2000-2699]: ")
            try:
                acl = int(acl)
                if 100 <= acl <= 199 or 2000 <= acl <= 2699:
                    break
                else:
                    print("Please enter a number between 100-199 or 2000-2699")
            except ValueError:
                print("Please enter a number between 100-199 or 2000-2699")
        elif selected_acl_type == "standard named":
            acl = input("Please Enter the name of the ACL: ")
            break
        elif selected_acl_type == "extended named":
            acl = input("Please Enter the name of the ACL: ")
            break

    return acl

def show_acl_running(cisco, acl_name, selected_acl_type):
    """Function to show running version of selected ACL"""

    with netmiko.ConnectHandler(**cisco) as ssh:
        output = ssh.send_command(f"show ip access-list {acl_name}")

    return output

def check_acl(cisco, acl_name, selected_acl_type):
    """Function to catch already existing ACL of a the same name in a different type"""

    output = show_acl_running(cisco=cisco, acl_name=acl_name, selected_acl_type=selected_acl_type)

    current_acl_type = None
    current_acl_name = None

    for line in output.splitlines():
        line = line.strip()

        if line.startswith("Standard IP access list "):
            current_acl_type = "standard named"
            current_acl_name = line.split()[-1]

        elif line.startswith("Extended IP access list "):
            current_acl_type = "extended named"
            current_acl_name = line.split()[-1]

        if current_acl_name == acl_name:
            if current_acl_type != selected_acl_type:
                return False, current_acl_type
            else:
                return True, current_acl_type

    return True, None

def get_acl_address(prompt):
    while True:
        ip_input = input(prompt).strip()

        if ip_input == 'any':
            return 'any'

        try:
            network = ipaddress.IPv4Network(ip_input, strict=False)

            if network.prefixlen == 32:
                return f"host {network.network_address}"
            else:
                return f"{network.network_address} {network.hostmask}"

        except ValueError:
            print("Please enter a valid IPv4 address/network in CIDR notation or any.")

def get_port(prompt):
    while True:
        port = input(prompt).strip()

        if port.isdigit():
            port_num = int(port)

            if 1 <= port_num <= 65535:
                return str(port_num)

        print("Please enter a valid port between 1 and 65535.")

def get_port_statement(direction):
    """Function to get the port used for source or destination port"""

    while True:
        use_port = input(
            f"Would you like to specify a {direction} port? [y/n]: "
        ).lower().strip()

        if use_port in ("n", "no"):
            return ""
        elif use_port in ("y","yes"):
            break
        else:
            print("Please enter y or n!")

    while True:
        operator = input(
        "Enter port operator [eq/neq/lt/gt/range]: ").lower().strip()

        if operator in ("eq", "neq", "lt", "gt", "range"):
            break
        else:
            print("Please enter eq, neq, lt, gt, or range!")

    if operator == "range":
        start_port = get_port("Enter starting port: ")
        end_port = get_port("Enter ending port: ")

        return f"{operator} {start_port} {end_port}"

    port = get_port("Enter port number: ")

    return f"{operator} {port}"

def get_acl_config(selected_acl_type):
    """Function to configure ACL"""

    while True:
        permit_deny = input("Would you like to permit or deny [permit/ deny]: ").lower()

        if permit_deny in ("permit", "deny"):
            break
        else:
            print("Please enter permit or deny!")

    if selected_acl_type in ("standard", "standard named"):
        source = get_acl_address(f"Please enter the source IP/network you would like to {permit_deny}: ")

        acl_entry = f"{permit_deny} {source}"

    else:
        while True:
            protocol = input("Please enter the protocol [ip/tcp/udp/icmp]: ").lower().strip()

            if protocol in ("ip", "tcp", "udp", "icmp"):
                break
            else:
                print("Please enter ip, tcp, udp, or icmp!")

        source = get_acl_address(f"Please enter the source IP/network you would like to {permit_deny}: ")

        source_port = ""

        if protocol in ("tcp", "udp"):
            source_port = get_port_statement("Source")
            
        destination = get_acl_address(f"Please enter the destination IP/network you would like to {permit_deny}: ")

        destination_port = ""

        if protocol in ("tcp", "udp"):
            destination_port = get_port_statement("destination")

        acl_parts = [
            permit_deny, 
            protocol, 
            source
            ]

        if source_port:
            acl_parts.append(source_port)

        acl_parts.append(destination)

        if destination_port:
            acl_parts.append(destination_port)

        acl_entry = " ".join(acl_parts)

        print("\nNew ACL Entry:")
        print(acl_entry)

    return acl_entry

def configure_acl(cisco, acl_config, acl_name, selected_acl_type):
    """Function to add the new ACL"""

    if selected_acl_type in ("standard", "standard named"):
        acl_type = "standard"
    elif selected_acl_type in ("extended", "extended named"):
        acl_type = "extended"

    command_set = [
        f"ip access-list {acl_type} {acl_name}",
        acl_config
    ]

    with netmiko.ConnectHandler(**cisco) as ssh:
        ssh.send_config_set(command_set)

    print("\nACL has been added")

def save_config(cisco):
    """Function to save the configuration"""

    with netmiko.ConnectHandler(**cisco) as ssh:
        ssh.save_config()

def main():
    while True:
        cisco = connect_info()
        ip = cisco["ip"]

        print(f"\nChecking reachability for {ip}\n")

        if ping_device(ip, count=1, timeout=2):
            print(f"!!!!!\n\n{ip} is reachable\n\n")
        else:
            print(f".....\n\n{ip} is not reachable\n\n")
            quit()

        selected_acl_type = get_acl_type()
        acl_name = get_acl_name(selected_acl_type=selected_acl_type)

        valid, existing_type = check_acl(cisco=cisco, acl_name=acl_name, selected_acl_type=selected_acl_type)

        if valid:
            pass
        else:
            print(f"ERROR: ACL '{acl_name}' already exists with a type of {existing_type} ACL.")
            print(f"You cannont create '{acl_name}' with a type of {selected_acl_type} ACL.")
            quit()

        print("Showing ACL current configuration:\n")
        output = show_acl_running(cisco=cisco, acl_name=acl_name, selected_acl_type=selected_acl_type)

        print(output)

        user_input(f"\nDo you want to configure a new rule for this {acl_name}? [y/n]: ")
        
        acl_config = get_acl_config(selected_acl_type=selected_acl_type)

        print(acl_config)

        user_input(f"\nDo you want to implement the new ACL rule for ACL {acl_name}? [y/n]: ")

        configure_acl(cisco=cisco, acl_config=acl_config, acl_name=acl_name, selected_acl_type=selected_acl_type)

        print("\nShowing updated ACL configuration:")
        output = show_acl_running(cisco=cisco, acl_name=acl_name, selected_acl_type=selected_acl_type)
        
        print(output)

        save_config(cisco=cisco)

        user_input("Would you like to change the ACL on another device? [y/n]: ")

if __name__ == "__main__":
    main()