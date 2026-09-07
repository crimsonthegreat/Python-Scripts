import argparse
import netmiko
import network_tools


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Adjust IP helper addresses on all Cisco IOS SVIs."
    )

    parser.add_argument(
        "files",
        nargs="*",
        metavar="FILE",
        help="Positional inventory file followed by IP helper file"
    )
    parser.add_argument(
        "-i",
        "--inventory",
        dest="inventory_file_explicit",
        help="CSV, YAML, or YML device inventory"
    )
    parser.add_argument(
        "-d",
        "--helper",
        dest="helper_file_explicit",
        help="CSV, YAML, or YML IP helper list"
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--replace",
        action="store_true",
        help="Remove unlisted helpers and add listed helpers"
    )
    mode.add_argument(
        "--remove",
        action="store_true",
        help="Remove only the helpers listed in the input file"
    )

    parser.add_argument(
        "--exclude-vlan",
        action="append",
        type=int,
        default=[],
        metavar="VLAN_ID",
        help="Exclude a VLAN; may be specified more than once"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show commands without changing or saving switches"
    )

    args = parser.parse_args()

    if len(args.files) > 2:
        parser.error("Specify no more than two positional files.")

    positional_files = list(args.files)
    args.inventory_file = args.inventory_file_explicit
    args.helper_file = args.helper_file_explicit

    if not args.inventory_file and positional_files:
        args.inventory_file = positional_files.pop(0)

    if not args.helper_file and positional_files:
        args.helper_file = positional_files.pop(0)

    if positional_files:
        parser.error(
            "A file was specified both positionally and with an explicit option."
        )

    if not args.inventory_file:
        parser.error(
            "An inventory file is required positionally or with -i/--inventory."
        )

    if not args.helper_file:
        parser.error(
            "An IP helper file is required positionally or with -d/--helper."
        )

    return args


def process_device(device, username, password, desired_helpers, mode,
                   excluded_vlans, dry_run):
    ip = device["ip"]

    print("\n" + "=" * 60)
    print(f"Processing Device: {ip}")
    print("=" * 60)

    if not network_tools.ping_device(ip):
        return {"ip": ip, "status": "failed", "reason": "Ping failed"}

    connection = network_tools.build_connection(device, username, password)

    try:
        with netmiko.ConnectHandler(**connection) as ssh:
            hostname = ssh.find_prompt().strip("#>")
            svis = network_tools.get_svi_helpers(ssh)

            if not svis:
                return {
                    "ip": ip,
                    "hostname": hostname,
                    "status": "skipped",
                    "reason": "No configured SVIs found"
                }

            command_sets = network_tools.build_helper_commands(
                svis=svis,
                desired_helpers=desired_helpers,
                mode=mode,
                excluded_vlans=excluded_vlans
            )

            if not command_sets:
                print(f"{hostname}: IP helpers already match the requested state.")
                return {
                    "ip": ip,
                    "hostname": hostname,
                    "status": "unchanged",
                    "reason": "Already compliant"
                }

            print(f"\n{hostname}: planned IP helper changes:")

            for commands in command_sets.values():
                for command in commands:
                    print(f"  {command}")

            network_tools.apply_helper_commands(
                ssh=ssh,
                command_sets=command_sets,
                dry_run=dry_run
            )

            if not dry_run:
                print("\nSaving configuration...")
                print(network_tools.save_config(ssh=ssh))

            return {
                "ip": ip,
                "hostname": hostname,
                "status": "dry-run" if dry_run else "success",
                "reason": ""
            }

    except netmiko.NetmikoAuthenticationException:
        return {"ip": ip, "status": "failed", "reason": "Authentication failure"}
    except netmiko.NetmikoTimeoutException:
        return {"ip": ip, "status": "failed", "reason": "Connection timeout"}
    except Exception as error:
        return {"ip": ip, "status": "failed", "reason": str(error)}


def main():
    args = get_arguments()

    try:
        desired_helpers = network_tools.load_helper_addresses(args.helper_file)
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"ERROR loading IP helpers: {error}")
        return

    devices = network_tools.get_devices(args.inventory_file)

    if not devices:
        print("No valid devices to process.")
        return

    mode = "replace" if args.replace else "remove" if args.remove else "ensure"
    username, password = network_tools.get_credentials()
    results = []

    for device in devices:
        results.append(
            process_device(
                device=device,
                username=username,
                password=password,
                desired_helpers=desired_helpers,
                mode=mode,
                excluded_vlans=args.exclude_vlan,
                dry_run=args.dry_run
            )
        )

    print("\n" + "=" * 60)
    print("IP HELPER UPDATE SUMMARY")
    print("=" * 60)

    for result in results:
        hostname = result.get("hostname", "Unknown")
        reason = f" - {result['reason']}" if result.get("reason") else ""
        print(f"[{result['status'].upper()}] {hostname} - {result['ip']}{reason}")


if __name__ == "__main__":
    main()
