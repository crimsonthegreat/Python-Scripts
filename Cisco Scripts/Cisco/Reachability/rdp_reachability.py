import argparse
import network_tools

print("\n" + "=" * 60)
print("This script can be used to test rdp to devices")
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

    return args


def process_device(
        device, 
        dev_num, 
        num_of_devices, 
        ):
    """Update passwords on a single device."""

    ip = device["ip"]

    print("\n" + "=" * 60)
    print(f"Processing Device {dev_num} of {num_of_devices}: {ip}")
    print("=" * 60)

    print(f"\nChecking RDP on {ip}:3389...")
    
    if not network_tools.check_tcp_port(ip, 3389):
        print(f"TCP/3389 is not reachable on {ip}.")

        return {
            "ip": ip,
            "status": "failed",
            "reason": "TCP/3389 unreachable",
        }

    print(f"RDP is reachable on {ip}:3389.")

    return {
        "ip": ip,
        "status": "success",
        "reason": ""
    }

def main():
    args = get_arguments()

    devices = network_tools.get_devices(
            inventory_file=args.inventory_file
        )

    results = []
    dev_num = 1
    
    for device in devices:

        result = process_device(
                    device=device,
                    dev_num=dev_num,
                    num_of_devices=len(devices)
        )

        dev_num += 1
                    
        results.append(result)

    print("\n")
    print("=" * 60)
    print("Ping Summary")
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
        print(
            f"  [SUCCESS] "
            f"{result['ip']}"
        )

    print(
            f"\nSkipped: {len(skipped)}"
        )
    
    for result in skipped:
        print(
            f"  [SKIPPED] "
            f"{result['ip']}"
        )

    print(
        f"\nFailed: {len(failed)}"
    )

    for result in failed:
        print(
            f"  [FAILED] "
            f"{result['ip']}"
        )

    log_file = network_tools.write_results_log(
                results=results,
                script_name="rdp_reachability"
            )

    print(f"\nResults written to: {log_file}")

if __name__ == "__main__":
    main()