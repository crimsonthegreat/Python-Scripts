import ipaddress
import csv
import yaml

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
    """Load devices from YAML inventory."""

    devices = []

    try:
        with open(filename, mode="r") as file:
            data = yaml.safe_load(file)

        if not data or "devices" not in data:
            print(
                "ERROR: YAML file must contain a 'devices' section."
            )
            return []

        for index, device in enumerate(
            data["devices"],
            start=1
        ):
            ip = str(
                device.get("ip", "")
            ).strip()

            hostname = str(
                device.get("hostname", "Unknown")
            ).strip()

            try:
                ipaddress.IPv4Address(ip)

            except ipaddress.AddressValueError:
                print(
                    f"Skipping invalid IP '{ip}' "
                    f"for device '{hostname}'."
                )
                continue

            device_type = device.get(
                "device_type",
                "cisco_ios"
            )

            # Preserve all fields from YAML
            device["ip"] = ip
            device["device_type"] = device_type

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

    print(
        f"\nLoaded {len(devices)} device(s) "
        f"from {filename}."
    )

    return devices

def filter_devices(devices, site=None):
    """Filter device inventory by optional criteria."""

    if site:
        devices = [
            device
            for device in devices
            if str(device.get("site", "")).lower()
            == site.lower()
        ]

    return devices