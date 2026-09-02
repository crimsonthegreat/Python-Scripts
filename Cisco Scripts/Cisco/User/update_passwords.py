import argparse
import getpass

import netmiko
import network_tools

print("\n" + "=" * 60)
print("This script can be used to update the enable and local-user secrets on Cisco IOS/IOS-XE devices")
print("=" * 60)

def get_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Update enable and local-user secrets "
            "on Cisco IOS/IOS-XE devices."
        )
    )

    parser.add_argument(
        "inventory_file",
        nargs="?",
        help="CSV or YAML device inventory file",
    )

    parser.add_argument(
        "-i",
        "--inventory",
        dest="inventory_file_explicit",
        help="CSV or YAML device inventory file",
    )

    parser.add_argument(
        "-s",
        "--site",
        nargs="+",
        help="Limit execution to one or more site codes",
    )

    parser.add_argument(
        "--username",
        help="Local username whose secret should be changed",
    )

    parser.add_argument(
        "--enable",
        action="store_true",
        help="Change the enable secret",
    )

    parser.add_argument(
        "--user",
        action="store_true",
        help="Change the local user secret",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show target devices without making changes",
    )

    args = parser.parse_args()

    if args.inventory_file and args.inventory_file_explicit:
        parser.error(
            "Specify inventory positionally or with "
            "--inventory, not both."
        )

    args.inventory_file = (
        args.inventory_file_explicit
        or args.inventory_file
    )

    if not args.enable and not args.user:
        parser.error(
            "Specify --enable, --user, or both."
        )

    if args.user and not args.username:
        parser.error(
            "--username is required when using --user."
        )

    return args


def process_device(
        device, 
        dev_num, 
        num_of_devices, 
        username, 
        password, 
        enable_secret, 
        local_username, 
        user_secret, 
        dry_run=False
        ):
    """Update passwords on a single device."""

    ip = device["ip"]
    
    print("\n" + "=" * 60)
    print(f"Processing Device {dev_num} of {num_of_devices}: {ip}")
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

            print(
                f"Connected to {hostname} ({ip})"
            )

            network_tools.set_device_passwords(
                ssh=ssh,
                enable_secret=enable_secret,
                username=local_username,
                user_secret=user_secret,
            )

            network_tools.save_config(ssh)

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

    username, password = (
        network_tools.get_credentials()
    )

    devices = network_tools.get_devices(
        inventory_file=args.inventory_file
    )

    devices = network_tools.filter_devices(
        devices,
        site=args.site,
    )

    if not devices:
        print("No matching devices found.")
        return

    enable_secret = None
    user_secret = None

    if args.enable:
        enable_secret = getpass.getpass(
            "New enable secret: "
        )

        confirm = getpass.getpass(
            "Confirm enable secret: "
        )

        if enable_secret != confirm:
            raise SystemExit(
                "Enable secrets do not match."
            )

    if args.user:
        user_secret = getpass.getpass(
            f"New secret for {args.username}: "
        )

        confirm = getpass.getpass(
            "Confirm user secret: "
        )

        if user_secret != confirm:
            raise SystemExit(
                "User secrets do not match."
            )

    print("\nDevices selected:")

    for device in devices:
        print(
            f"  {device.get('hostname', ''):<20} "
            f"{device['ip']:<16} "
            f"{device.get('site', '')}"
        )

    if args.dry_run:
        print("\nDRY RUN - no configurations will change.")

    else:
        network_tools.user_input(
            "\nProceed with password change? [y/n]: "
        )

    results = []
    dev_num = 1

    for device in devices:
        result = process_device(
            device=device,
            dev_num=dev_num,
            num_of_devices=len(devices),
            username=username,
            password=password,
            enable_secret=enable_secret,
            local_username=(
                args.username if args.user else None
            ),
            user_secret=user_secret,
            dry_run=args.dry_run,
        )
        dev_num += 1
        
        results.append(result)

    # Final report
    print("\n")
    print("=" * 60)
    print("Password Update Summary")
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

    log_file = network_tools.write_results_csv(
        results=results,
        script_name="update_passwords",
    )

    print(f"\nResults written to: {log_file}")


if __name__ == "__main__":
    main()