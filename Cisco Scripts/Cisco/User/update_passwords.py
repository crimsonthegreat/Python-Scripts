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

    parser.add_argument(
    "--env",
    metavar="FILE",
    help="Load the new username, user secret and enable secret from a .env file"),

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

    if args.user and not args.username and not args.env:
        parser.error(
            "--username is required when using --user "
            "unless --env is specified."
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

            hostname = ssh.find_prompt().replace("#","").replace(">","")

            print(f"Connected to {hostname} ({ip})")

            if dry_run:
                print(
                    f"DRY RUN: No changes made to "
                    f"{hostname} ({ip})."
                )

                return {
                    "ip": ip,
                    "hostname": hostname,
                    "site": device.get("site", ""),
                    "status": "skipped",
                    "reason": "Dry run - no changes made",
                }

            print(f"\nUpdating credentials on {hostname}...")

            network_tools.set_device_passwords(
                ssh=ssh,
                enable_secret=enable_secret,
                username=local_username,
                user_secret=user_secret,
            )

            print("Verifying password configuration...")

            verification = (
                network_tools.verify_password_configuration(
                    ssh=ssh,
                    username=local_username,
                    verify_enable=(
                        enable_secret is not None
                    ),
                )
            )

            if not verification["valid"]:

                failures = []

                if local_username:

                    if not verification["user_privilege_15"]:
                        failures.append(
                            "User is not privilege 15"
                        )

                    if not verification["user_scrypt"]:
                        failures.append(
                            "User secret is not Type 9/scrypt"
                        )

                if enable_secret:

                    if not verification["enable_scrypt"]:
                        failures.append(
                            "Enable secret is not Type 9/scrypt"
                        )

                reason = "; ".join(failures)

                print(
                    f"Verification failed on {hostname}: "
                    f"{reason}"
                )

                return {
                    "ip": ip,
                    "hostname": hostname,
                    "site": device.get("site", ""),
                    "status": "failed",
                    "reason": reason,
                }

            print("Password configuration verified.")

            network_tools.save_config(ssh)

            return {
                            "ip": ip,
                            "hostname": hostname,
                            "site": device.get("site", ""),
                            "status": "success",
                            "reason": ""
                        }

    except netmiko.NetmikoAuthenticationException:
    
            print(
                f"Authentication failed for {ip}."
            )
    
            return {
                "ip": ip,
                "hostname": hostname,
                "site": device.get("site", ""),
                "status": "failed",
                "reason": "Authentication failure"
            }
    
    except netmiko.NetmikoTimeoutException:

        print(
            f"Connection to {ip} timed out."
        )

        return {
            "ip": ip,
            "hostname": hostname,
            "site": device.get("site", ""),
            "status": "failed",
            "reason": "Connection timeout"
        }

    except Exception as e:

        print(
            f"Unexpected error on {ip}: {e}"
        )

        return {
            "ip": ip,
            "hostname": hostname,
            "site": device.get("site", ""),
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

    if args.env:
        try:
            new_credentials = (
                network_tools.load_new_credentials(
                    args.env
                )
            )

        except (FileNotFoundError, ValueError) as error:
            raise SystemExit(
                f"Unable to load credentials: {error}"
            )

        if args.user:
            local_username = (
                new_credentials["username"]
            )

            user_secret = (
                new_credentials["user_secret"]
            )

            if not local_username:
                raise SystemExit(
                    "NEW_DEVICE_USERNAME is missing "
                    "from the .env file."
                )

            if not user_secret:
                raise SystemExit(
                    "NEW_DEVICE_PASSWORD is missing "
                    "from the .env file."
                )

        if args.enable:
            enable_secret = (
                new_credentials["enable_secret"]
            )

            if not enable_secret:
                raise SystemExit(
                    "NEW_ENABLE_PASSWORD is missing "
                    "from the .env file."
                )

    else:

        if args.user:
            local_username = args.username

            user_secret = getpass.getpass(
                f"New secret for {local_username}: "
            )

            confirm = getpass.getpass(
                "Confirm user secret: "
            )

            if user_secret != confirm:
                raise SystemExit(
                    "User secrets do not match."
                )

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

        result = process_device(
            device=device,
            dev_num=dev_num,
            num_of_devices=len(devices),
            username=username,
            password=password,
            enable_secret=enable_secret,
            local_username=local_username,
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

    log_file = network_tools.write_results_log(
            results=results,
            script_name="remove_update_add_acc_class"
        )
    
    log_file = network_tools.write_results_csv(
        results=results,
        script_name="update_passwords",
    )

    print(f"\nResults written to: {log_file}")


if __name__ == "__main__":
    main()