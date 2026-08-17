import netmiko
import getpass
import ipaddress
import subprocess
import csv
import argparse
import yaml
import re

print("\n" + "=" * 60)
print("This script can be used to update the ACL on a network device" + "\n" + "=" * 60)


def get_credentials():
    """Get credentials once for all devices."""

    username = input("Enter Username: ").strip()
    password = getpass.getpass("Enter Password: ")

    return username, password

def get_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Update ACLs on Cisco network devices."
    )

    parser.add_argument(
    "inventory_file",
    nargs="?",
    help="Optional CSV or YAML inventory file"
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="inventory_file_explicit",
        help="CSV or YAML inventory file"
    )

    args = parser.parse_args()

    # Prevent both from being used at the same time
    if args.inventory_file and args.inventory_file_explicit:
        parser.error(
            "Specify the CSV file either positionally or with --csv, not both."
        )

    # Normalize into one variable
    args.inventory_file = (
        args.inventory_file_explicit
        or args.inventory_file
    )

    return args

def get_devices(inventory_file=None):
    """Get a single device or load devices from CSV/YAML inventory."""

    if not inventory_file:
        while True:
            ip = input(
                "Please enter the device IP address: "
            ).strip()

            try:
                ipaddress.IPv4Address(ip)
                break

            except ipaddress.AddressValueError:
                print("Please enter a valid IPv4 address.")

        return [
            {
                "ip": ip,
                "device_type": "cisco_ios"
            }
        ]

    extension = inventory_file.lower()

    if extension.endswith(".csv"):
        return load_csv_devices(inventory_file)

    elif extension.endswith((".yaml", ".yml")):
        return load_yaml_devices(inventory_file)

    else:
        print(
            "ERROR: Inventory file must be CSV, YAML, or YML."
        )
        return []

def load_csv_devices(filename):
    """Load devices from CSV."""

    devices = []

    try:
        with open(filename, mode="r", newline="") as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames or "ip" not in reader.fieldnames:
                print(
                    "ERROR: CSV must contain an 'ip' column."
                )
                return []

            for row_number, row in enumerate(reader, start=2):

                ip = row["ip"].strip()

                try:
                    ipaddress.IPv4Address(ip)

                except ipaddress.AddressValueError:
                    print(
                        f"Skipping invalid IP '{ip}' "
                        f"on row {row_number}."
                    )
                    continue

                device_type = row.get(
                    "device_type",
                    "cisco_ios"
                ).strip()

                if not device_type:
                    device_type = "cisco_ios"

                devices.append(
                    {
                        "ip": ip,
                        "device_type": device_type
                    }
                )

    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found.")
        return []

    return devices

def load_yaml_devices(filename):
    """Load devices from site-based YAML inventory."""

    devices = []

    try:
        with open(filename, mode="r") as file:
            data = yaml.safe_load(file)

        if not data or "sites" not in data:
            print(
                "ERROR: YAML file must contain a top-level 'sites' section."
            )
            return []

        for site_name, site_data in data["sites"].items():

            if not site_data:
                continue

            site_devices = site_data.get("devices", [])

            for device in site_devices:

                ip = str(
                    device.get("ip", "")
                ).strip()

                try:
                    ipaddress.IPv4Address(ip)

                except ipaddress.AddressValueError:
                    print(
                        f"Skipping invalid IP '{ip}' "
                        f"at site '{site_name}'."
                    )
                    continue

                # Default device type if omitted
                device_type = device.get(
                    "device_type",
                    "cisco_ios"
                )

                # Preserve all YAML fields
                device["ip"] = ip
                device["device_type"] = device_type

                # Automatically populate site
                device.setdefault(
                    "site",
                    site_name
                )

                devices.append(device)

    except FileNotFoundError:
        print(
            f"ERROR: File '{filename}' not found."
        )
        return []

    except yaml.YAMLError as e:
        print(
            f"ERROR parsing YAML file: {e}"
        )
        return []

    return devices

def build_connection(device, username, password):
    """Build Netmiko connection dictionary."""

    return {
        "device_type": device.get(
            "device_type",
            "cisco_ios"
        ),
        "ip": device["ip"],
        "username": username,
        "password": password
    }


def ping_device(ip, count=1, timeout=2):
    """Ping a device."""

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
                    return acl
                else:
                    print("Please enter a number between 1-99 or 1300-1999")
            except ValueError:
                print("Please enter a number between 1-99 or 1300-1999")
        elif selected_acl_type == "extended":
            acl = input("Please Enter the number of the ACL [100-199 or 2000-2699]: ")
            try:
                acl = int(acl)
                if 100 <= acl <= 199 or 2000 <= acl <= 2699:
                    return acl
                else:
                    print("Please enter a number between 100-199 or 2000-2699")
            except ValueError:
                print("Please enter a number between 100-199 or 2000-2699")
        elif selected_acl_type in ("standard named", "extended named"):
            acl = input("Please Enter the name of the ACL: ").strip()

            if acl:
                return acl
            else:
                print("The ACL name cannot be blank")

def show_acl_running(ssh, acl_name):
    """Function to show running version of selected ACL"""

    return ssh.send_command(f"show ip access-list {acl_name}")

def find_terminal_deny(acl_output):
    """Find an explicit terminal deny rule in the ACL.

    Supports:
      Standard: deny any log
      Extended: deny ip any any log

    Returns the sequence number if found, otherwise None.
    """

    patterns = [
        # Standard ACL
        r"^\s*(\d+)\s+deny\s+any\s+log\s*$",

        # Extended ACL
        r"^\s*(\d+)\s+deny\s+ip\s+any\s+any\s+log\s*$"
    ]

    for line in acl_output.splitlines():

        for pattern in patterns:
            match = re.match(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:
                return match.group(1)

    return None

def remove_terminal_deny(ssh, acl_name, selected_acl_type, sequence):
    """Remove explicit terminal deny ACE from ACL."""

    if selected_acl_type in ("standard", "standard named"):
        acl_type = "standard"
    else:
        acl_type = "extended"

    command_set = [
        f"ip access-list {acl_type} {acl_name}",
        f"no {sequence}"
    ]

    output = ssh.send_config_set(command_set)

    return output

def check_acl(ssh, acl_name, selected_acl_type):
    """Function to catch already existing ACL of a the same name in a different type"""

    output = show_acl_running(ssh=ssh, acl_name=acl_name)

    if selected_acl_type in (
        "standard",
        "standard named"
    ):
        requested_type = "standard"

    else:
        requested_type = "extended"

    for line in output.splitlines():

        line = line.strip()

        if line.startswith("Standard IP access list "):
            current_acl_type = "standard"
            current_acl_name = line.split()[-1]

        elif line.startswith("Extended IP access list "):
            current_acl_type = "extended"
            current_acl_name = line.split()[-1]

        else:
            continue

        if str(current_acl_name).lower() == str(acl_name).lower():

            if current_acl_type != requested_type:
                return False, current_acl_type

            return True, current_acl_type

    return True, None

def get_acl_address(prompt):
    """Function to get information on and format the ip address for an ACL"""

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
    """Function to validate TCP/UDP port"""

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
        permit_deny = input("Would you like to permit or deny [permit/ deny]: ").lower().strip()

        if permit_deny in ("permit", "deny"):
            break
        else:
            print("Please enter permit or deny!")

    #Standard ACL
    if selected_acl_type in ("standard", "standard named"):
        source = get_acl_address(f"Please enter the source IP/network you would like to {permit_deny}: ")

        acl_entry = f"{permit_deny} {source}"

    #Extended ACL
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

def configure_acl(ssh, acl_config, acl_name, selected_acl_type):
    """Function to add the new ACL"""

    if selected_acl_type in ("standard", "standard named"):
        acl_type = "standard"
    elif selected_acl_type in ("extended", "extended named"):
        acl_type = "extended"

    command_set = [
        f"ip access-list {acl_type} {acl_name}",
        acl_config
    ]

    return ssh.send_config_set(command_set)

def save_config(ssh):
    """Function to save the configuration"""

    return ssh.save_config()

def process_device(device, username, password, acl_name, selected_acl_type, acl_config):
    """Process one device using one SSH connection."""

    ip = device["ip"]

    print("\n" + "=" * 60)
    print(f"Processing Device: {ip}")
    print("=" * 60)

    print(f"\nChecking reachability for {ip}...")

    if not ping_device(ip):

        print(f"{ip} is not reachable.")

        return {
            "ip": ip,
            "status": "failed",
            "reason": "Ping failed"
        }

    print(f"{ip} is reachable.")

    cisco = build_connection(
        device=device,
        username=username,
        password=password
    )

    try:

        # ONE SSH CONNECTION FOR THE ENTIRE DEVICE
        with netmiko.ConnectHandler(**cisco) as ssh:

            hostname = ssh.find_prompt().replace(
                "#",
                ""
            ).replace(
                ">",
                ""
            )

            print(
                f"Connected to {hostname} ({ip})"
            )

            # Check ACL type
            valid, existing_type = check_acl(
                ssh=ssh,
                acl_name=acl_name,
                selected_acl_type=selected_acl_type
            )

            if not valid:

                print(f"\nERROR: ACL '{acl_name}' already exists as {existing_type}.")

                return {
                    "ip": ip,
                    "status": "failed",
                    "reason": (
                        f"ACL exists as "
                        f"{existing_type}"
                    )
                }

            # Show current ACL
            print("\nCurrent ACL configuration:\n")

            before_output = show_acl_running(ssh=ssh, acl_name=acl_name)

            print(before_output)

            terminal_deny_sequence = find_terminal_deny(before_output)

            if terminal_deny_sequence:

                print(f"\nFound terminal deny at sequence {terminal_deny_sequence}.")

                print("Removing terminal deny before adding the new ACL entry...")

                remove_output = remove_terminal_deny(
                    ssh=ssh,
                    acl_name=acl_name,
                    selected_acl_type=selected_acl_type,
                    sequence=terminal_deny_sequence
                )

                print(remove_output)

            print("\nApplying ACL configuration...")

            config_output = configure_acl(
                ssh=ssh,
                acl_config=acl_config,
                acl_name=acl_name,
                selected_acl_type=selected_acl_type
            )

            print(config_output)

            # Verify
            print("\nVerifying ACL configuration:\n")

            after_output = show_acl_running(ssh=ssh, acl_name=acl_name)

            print(after_output)

            # Save
            print("\nSaving configuration...")

            save_output = save_config(ssh=ssh)

            print(save_output)

            return {
                "ip": ip,
                "hostname": hostname,
                "status": "success",
                "reason": ""
            }

    except netmiko.NetmikoAuthenticationException:

        print(
            f"Authentication failed for {ip}."
        )

        return {
            "ip": ip,
            "status": "failed",
            "reason": "Authentication failure"
        }

    except netmiko.NetmikoTimeoutException:

        print(
            f"Connection to {ip} timed out."
        )

        return {
            "ip": ip,
            "status": "failed",
            "reason": "Connection timeout"
        }

    except Exception as e:

        print(
            f"Unexpected error on {ip}: {e}"
        )

        return {
            "ip": ip,
            "status": "failed",
            "reason": str(e)
        }
            
def main():

    args = get_arguments()

    # Credentials only once
    username, password = get_credentials()

    devices = get_devices(inventory_file=args.inventory_file)

    if not devices:
        print("No valid devices to process.")
        return

    print(f"\n{len(devices)} device(s) selected:")

    for device in devices:
        print(f"  {device['ip']}")

    # ACL information only once
    selected_acl_type = get_acl_type()

    acl_name = get_acl_name(selected_acl_type)

    acl_config = get_acl_config(selected_acl_type)

    print("\n" + "=" * 60)
    print("PROPOSED ACL CHANGE")
    print("=" * 60)

    print(f"ACL Type : {selected_acl_type}")

    print(f"ACL Name : {acl_name}")

    print(f"ACL Entry: {acl_config}")

    print("\nTarget Devices:")

    for device in devices:
        print(f"  {device['ip']}")

    user_input("\nApply this ACL change? [y/n]: ")

    results = []

    # Process every device
    for device in devices:

        result = process_device(
            device=device,
            username=username,
            password=password,
            acl_name=acl_name,
            selected_acl_type=selected_acl_type,
            acl_config=acl_config
        )

        results.append(result)

    # Final report
    print("\n")
    print("=" * 60)
    print("ACL UPDATE SUMMARY")
    print("=" * 60)

    successful = [
        result
        for result in results
        if result["status"] == "success"
    ]

    failed = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    print(
        f"\nSuccessful: {len(successful)}"
    )

    for result in successful:

        hostname = result.get(
            "hostname",
            "Unknown"
        )

        print(
            f"  [SUCCESS] "
            f"{hostname} - {result['ip']}"
        )

    print(
        f"\nFailed: {len(failed)}"
    )

    for result in failed:

        print(
            f"  [FAILED] "
            f"{result['ip']} - "
            f"{result['reason']}"
        )

if __name__ == "__main__":
    main()