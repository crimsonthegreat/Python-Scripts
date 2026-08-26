import netmiko
import argparse
import network_tools

print("\n" + "=" * 60)
print("Update ACL on VTY Lines" + "\n" + "=" * 60)

def get_arguments():
    parser = argparse.ArgumentParser(
        description="Update ACLs on Cisco devices."
    )

    parser.add_argument(
        "inventory_file",
        nargs="?",
        help="CSV or YAML inventory file",
    )

    parser.add_argument(
        "acl_rules_file",
        nargs="?",
        help="CSV or YAML file containing ACL rules"
    )

    parser.add_argument(
        "-i",
        "--inventory",
        dest="inventory_file_explicit",
        help="CSV or YAML inventory file",
    )

    parser.add_argument(
            "-a",
            "--acl-rules",
            dest="acl_rules_file_explicit",
            help="CSV or YAML file containing ACL rules"
        )

    parser.add_argument(
        "-s",
        "--site",
        help="Limit execution to devices assigned to this site",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without configuring devices",
    )

    args = parser.parse_args()

    # Prevent duplicate inventory arguments
    if args.inventory_file and args.inventory_file_explicit:
        parser.error(
            "Specify the inventory file either positionally "
            "or with --inventory, not both."
        )

    # Prevent duplicate ACL rules arguments
    if args.acl_rules_file and args.acl_rules_file_explicit:
        parser.error(
            "Specify the ACL rules file either positionally "
            "or with --acl-rules, not both."
        )

    # Normalize arguments
    args.inventory_file = (
        args.inventory_file_explicit
        or args.inventory_file
    )

    args.acl_rules_file = (
        args.acl_rules_file_explicit
        or args.acl_rules_file
    )

    return args

def process_device(device, username, password, acl_name, acl_type, acl_commands, dry_run=False):
    """Process one device using one SSH connection."""

    ip = device["ip"]

    print("\n" + "=" * 60)
    print(f"Processing Device: {ip}")
    print("=" * 60)

    print(f"\nChecking reachability for {ip}...")

    if not network_tools.ping_device(ip):

        print(f"{ip} is not reachable.")

        return {
            "ip": ip,
            "status": "failed",
            "reason": "Ping failed"
        }

    print(f"{ip} is reachable.")

    cisco = network_tools.build_connection_param(
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

            print(f"\nConnected to {hostname} ({ip})")

            print("\nShowing existing VTY line configuration\n")

            vty_lines = network_tools.get_vty_lines(ssh=ssh)

            if not vty_lines:
                raise ValueError("No VTY line configuration was found on the device.")

            acl_references = network_tools.get_vty_acl_references(ssh=ssh, acl_name=acl_name)

            if not acl_references:
                print(f"\nACL '{acl_name}' is not applied to any VTY lines.")
            else:
                print("\nACL is currently applied to the following VTY lines:")

                for reference in acl_references:
                    print(reference["line"])
                    print(reference["command"])
                    print("!")

            if dry_run:
                print("\nDRY RUN - planned configuration sequence:")

                for reference in acl_references:
                    print(f"  {reference['line']}")
                    print(f"  no {reference['command']}")

                print(f"  no ip access-list {acl_type} {acl_name}")

                for command in acl_commands:
                    print(f"  {command}")

                for line in vty_lines:
                    print(f"  {line}")
                    print(f"  access-class {acl_name} in")

                return {
                    "ip": ip,
                    "hostname": hostname,
                    "status": "success",
                    "reason": "Dry run completed"
                }

            if acl_references:
                print("\nRemoving existing VTY access-class references...")
                network_tools.remove_vty_acl_references(
                    ssh=ssh,
                    references=acl_references
                )

            print(f"\nRemoving existing ACL '{acl_name}'...")
            network_tools.remove_acl(
                ssh=ssh,
                acl_name=acl_name,
                acl_type=acl_type
            )

            print(f"\nApplying updated ACL '{acl_name}'...")
            ssh.send_config_set(acl_commands)

            print("\nApplying the ACL to all VTY lines...")
            network_tools.apply_acl_to_all_vty_lines(
                    ssh=ssh,
                    acl_name=acl_name,
                    vty_lines=vty_lines,
                    direction="in"
            )
            
            # Save
            print("\nSaving configuration...\n")

            save_output = network_tools.save_config(ssh=ssh)

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

    if not args.acl_rules_file:
        print(
            "ERROR: An ACL rules file is required.\n"
            "Usage: python remove_update_add_acc_class.py "
            "<inventory.yaml|csv> <acl_rules.yaml|csv>"
        )
        return

    try:
        imported_rules = network_tools.load_acl_rules(args.acl_rules_file)
        command_sets = network_tools.build_acl_command_sets(imported_rules)
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"ERROR loading ACL rules: {error}")
        return

    if len(command_sets) != 1:
        print(
            "ERROR: This workflow requires exactly one ACL in the ACL rules file. "
            f"Found {len(command_sets)}."
        )
        return

    (acl_type, acl_name), acl_commands = next(iter(command_sets.items()))

    username,password = network_tools.get_credentials()

    devices = network_tools.get_devices(inventory_file=args.inventory_file)

    devices = network_tools.filter_devices(devices, site=args.site)

    if not devices:
        if args.site:
            print(
                f"No devices found matching site "
                f"'{args.site}'."
            )
        else:
            print("No valid devices to process.")

        return

    print(f"\n{len(devices)} device(s) selected:")

    for device in devices:
        print(f"  {device['ip']}")

    results = []
    
    # Process every device
    for device in devices:

        result = process_device(
            device=device,
            username=username,
            password=password,
            acl_name=acl_name,
            acl_type=acl_type,
            acl_commands=acl_commands,
            dry_run=args.dry_run,
        )

        results.append(result)

    # Final report
    print("\n")
    print("=" * 60)
    print("ACCESS CLASS REMOVAL UPDATE SUMMARY")
    print("=" * 60)

    successful = [
        result
        for result in results
        if result["status"] == "success"
    ]

    skipped = [
            result
            for result in results
            if result["status"] == "skipped"
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
        f"\nSkipped: {len(skipped)}"
    )

    for result in skipped:

        hostname = result.get(
            "hostname",
            "Unknown"
        )

        print(
            f"  [SKIPPED] "
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
