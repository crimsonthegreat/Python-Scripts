import netmiko
import network_tools
import argparse

print("\n" + "=" * 60)
print("This script can be used to update the ACL on a network device")
print("=" * 60)

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
        "-i",
        "--inventory",
        dest="inventory_file_explicit",
        help="CSV or YAML inventory file"
    )

    args = parser.parse_args()

    # Prevent both from being used at the same time
    if args.inventory_file and args.inventory_file_explicit:
        parser.error(
            "Specify the inventory file either positionally "
            "or with --file, not both."
        )

    # Normalize into one variable
    args.inventory_file = (
        args.inventory_file_explicit
        or args.inventory_file
    )

    return args

def process_device(device, username, password, acl_name, selected_acl_type, acl_config):
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

    cisco = network_tools.build_connection(
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
            valid, existing_type = network_tools.check_acl(
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

            before_output = network_tools.show_acl_running(ssh=ssh, acl_name=acl_name)

            print(before_output)

            terminal_deny_sequence = network_tools.find_terminal_deny(before_output)

            if terminal_deny_sequence:

                print(f"\nFound terminal deny at sequence {terminal_deny_sequence}.")

                print("Removing terminal deny before adding the new ACL entry...")

                remove_output = network_tools.remove_terminal_deny(
                    ssh=ssh,
                    acl_name=acl_name,
                    selected_acl_type=selected_acl_type,
                    sequence=terminal_deny_sequence
                )

                print(remove_output)

            print("\nApplying ACL configuration...")

            config_output = network_tools.configure_acl(
                ssh=ssh,
                acl_config=acl_config,
                acl_name=acl_name,
                selected_acl_type=selected_acl_type
            )

            print(config_output)

            # Verify
            print("\nVerifying ACL configuration:\n")

            after_output = network_tools.show_acl_running(ssh=ssh, acl_name=acl_name)

            print(after_output)

            # Save
            print("\nSaving configuration...")

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

    # Credentials only once
    username, password = network_tools.get_credentials()

    devices = network_tools.get_devices(inventory_file=args.inventory_file)

    if not devices:
        print("No valid devices to process.")
        return

    print(f"\n{len(devices)} device(s) selected:")

    for device in devices:
        print(f"  {device['ip']}")

    # ACL information only once
    selected_acl_type = network_tools.get_acl_type()

    acl_name = network_tools.get_acl_name(selected_acl_type)

    acl_config = network_tools.get_acl_config(selected_acl_type)

    print("\n" + "=" * 60)
    print("PROPOSED ACL CHANGE")
    print("=" * 60)

    print(f"ACL Type : {selected_acl_type}")

    print(f"ACL Name : {acl_name}")

    print(f"ACL Entry: {acl_config}")

    print("\nTarget Devices:")

    for device in devices:
        print(f"  {device['ip']}")

    network_tools.user_input("\nApply this ACL change? [y/n]: ")

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