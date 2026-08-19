import re
import netmiko
import ipaddress

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

def get_vty_acl_references(ssh, acl_name):
    """Find VTY access-class statements referencing the ACL."""

    output = ssh.send_command(
        "show running-config | section ^line vty"
    )

    references = []

    current_line = None

    for line in output.splitlines():

        stripped = line.strip()

        if stripped.startswith("line vty "):
            current_line = stripped
            continue

        if stripped.startswith("access-class "):

            parts = stripped.split()

            # access-class ACL_NAME in
            if len(parts) >= 3:

                configured_acl = parts[1]

                if configured_acl.lower() == str(acl_name).lower():

                    references.append(
                        {
                            "line": current_line,
                            "command": stripped
                        }
                    )

    return references

def get_vty_lines(ssh):
    """Return every configured VTY line or line range on the device."""

    output = ssh.send_command(
        "show running-config | section ^line vty"
    )

    vty_lines = []

    for line in output.splitlines():

        stripped = line.strip()

        if stripped.startswith("line vty ") and stripped not in vty_lines:
            vty_lines.append(stripped)

    return vty_lines

def remove_vty_acl_references(ssh, references):
    """Remove ACL access-class commands from VTY lines."""

    outputs = []

    for reference in references:

        command_set = [
            reference["line"],
            f"no {reference['command']}"
        ]

        output = ssh.send_config_set(command_set)

        outputs.append(output)

    return outputs

def restore_vty_acl_references(ssh, references):
    """Restore the exact VTY access-class statements captured earlier."""

    outputs = []

    for reference in references:

        command_set = [
            reference["line"],
            reference["command"]
        ]

        outputs.append(ssh.send_config_set(command_set))

    return outputs

def apply_acl_to_all_vty_lines(ssh, acl_name, vty_lines, direction="in"):
    """Apply an ACL access-class to every discovered VTY line range."""

    if direction not in ("in", "out"):
        raise ValueError("VTY access-class direction must be 'in' or 'out'.")

    outputs = []

    for line in vty_lines:

        command_set = [
            line,
            f"access-class {acl_name} {direction}"
        ]

        outputs.append(ssh.send_config_set(command_set))

    return outputs

def remove_acl(ssh, acl_name, acl_type):
    """Remove an entire named or numbered ACL using named ACL syntax."""

    if acl_type not in ("standard", "extended"):
        raise ValueError("ACL type must be standard or extended.")

    return ssh.send_config_set([
        f"no ip access-list {acl_type} {acl_name}"
    ])

def add_vty_acl_references(ssh, acl_name):
    """Remove ACL access-class commands from VTY lines."""

    command_set = [
        "line vty 0 15",
        f"access-class {acl_name} in"
    ]

    output = ssh.send_config_set(command_set)

    return output
