import netmiko
import getpass
import ipaddress
import subprocess
import csv
import argparse
import yaml
import re

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
    """User prompts to continue"""
    
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

def save_config(ssh):
    """Function to save the configuration"""

    return ssh.save_config()