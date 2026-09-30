import argparse
import getpass
import netmiko
import network_tools

print("\n" + "=" * 60)
print("This script can be used to update the snmpv3 configuration on Cisco IOS/IOS-XE devices")
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
        "config_file",
        nargs="?",
        help="SNMPv3 YAML desired-state file",
    )

    parser.add_argument(
        "-i",
        "--inventory",
        dest="inventory_file_explicit",
        help="CSV or YAML device inventory file",
    )

    parser.add_argument(
        "-c", 
        "--config", 
        dest="config_explicit",
        help="SNMPv3 YAML desired-state file"
    )

    parser.add_argument(
        "-s",
        "--site",
        nargs="+",
        help="Limit execution to one or more site codes",
    )

    parser.add_argument(
        "--no-save", 
        action="store_true", 
        help="Apply but do not write memory"
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

    if args.config_file and args.config_explicit:
        parser.error("Specify config positionally or with --config, not both")

    args.config_file = (
        args.config_explicit 
        or args.config_file
    )

    if not args.config_file:
        parser.error("An SNMPv3 config file is required")

    return args

def process_device(
        device, 
        dev_num, 
        num_of_devices, 
        username, 
        password, 
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
            
            print(f"\nUpdating SNMPv3 Configuration on {hostname}...")
            
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