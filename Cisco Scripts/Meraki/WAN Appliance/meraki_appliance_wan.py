#!/usr/bin/env python3

import os
import sys
import meraki
from dotenv import load_dotenv
from pathlib import Path
import yaml
import csv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
YAML_FILE = SCRIPT_DIR / "meraki_mx_wan_inventory.yaml"
CSV_FILE = SCRIPT_DIR / "meraki_mx_wan_inventory.csv"

print(f"Loading .env: {ENV_FILE}")
print(f".env exists: {ENV_FILE.exists()}")

load_dotenv(dotenv_path=ENV_FILE, override=True)

API_KEY = os.getenv("MERAKI_DASHBOARD_API_KEY")
ORG_ID = os.getenv("MERAKI_ORG_ID")

print(f"API key loaded: {bool(API_KEY)}")
print(f"Org ID loaded: {bool(ORG_ID)}")

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def safe(value):
    """
    Convert None values returned by the Meraki API into an empty string.
    Also converts other values to strings for safe formatting.
    """
    return "" if value is None else str(value)

# ---------------------------------------------------------------------------
# Validate Configuration
# ---------------------------------------------------------------------------

if not API_KEY:
    print("ERROR: MERAKI_DASHBOARD_API_KEY environment variable is not set.")
    print()
    print("Set it with:")
    print('export MERAKI_DASHBOARD_API_KEY="your_api_key"')
    sys.exit(1)

if ORG_ID == "YOUR_ORGANIZATION_ID":
    print("ERROR: Set ORG_ID in the script.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Connect to Meraki Dashboard
# ---------------------------------------------------------------------------

dashboard = meraki.DashboardAPI(
    API_KEY,
    suppress_logging=True
)


# ---------------------------------------------------------------------------
# Get Networks
# ---------------------------------------------------------------------------

print("Retrieving Meraki networks...")

networks = dashboard.organizations.getOrganizationNetworks(
    ORG_ID,
    total_pages="all"
)

network_names = {
    network["id"]: network["name"]
    for network in networks
}


# ---------------------------------------------------------------------------
# Get Organization Devices
#
# We use this to obtain the MX device names because the appliance uplink
# status response is primarily focused on serial/model/network/uplink data.
# ---------------------------------------------------------------------------

print("Retrieving Meraki devices...")

devices = dashboard.organizations.getOrganizationDevices(
    ORG_ID,
    total_pages="all"
)

device_names = {
    device["serial"]: device.get("name") or ""
    for device in devices
}


# ---------------------------------------------------------------------------
# Get MX Uplink Status
# ---------------------------------------------------------------------------

print("Retrieving MX WAN information...")
print()

uplink_statuses = dashboard.appliance.getOrganizationApplianceUplinkStatuses(
    ORG_ID,
    total_pages="all"
)


# ---------------------------------------------------------------------------
# Build Inventory
# ---------------------------------------------------------------------------

inventory = {"devices": []}

for device in uplink_statuses:
    serial = device.get("serial")

    mx = {
        "hostname": device_names.get(serial, ""),
        "network": network_names.get(device.get("networkId"), ""),
        "model": device.get("model"),
        "serial": serial,
        "uplinks": {}
    }

    for uplink in device.get("uplinks", []):
        interface = uplink.get("interface")

        if not interface:
            continue

        uplink_data = {
            "ip": uplink.get("ip"),
            "public_ip": uplink.get("publicIp"),
            "status": uplink.get("status")
        }

        # Remove fields with null values
        uplink_data = {
            key: value
            for key, value in uplink_data.items()
            if value is not None
        }

        mx["uplinks"][interface] = uplink_data

    inventory["devices"].append(mx)

# ---------------------------------------------------------------------------
# Write YAML
# ---------------------------------------------------------------------------

with open(YAML_FILE, "w") as file:
    yaml.safe_dump(
        inventory,
        file,
        sort_keys=False,
        default_flow_style=False
    )

# ---------------------------------------------------------------------------
# Write CSV
# ---------------------------------------------------------------------------

fieldnames = [
    "hostname",
    "network",
    "model",
    "serial",
    "wan1_ip",
    "wan1_public_ip",
    "wan1_status",
    "wan2_ip",
    "wan2_public_ip",
    "wan2_status"
]

with open(CSV_FILE, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for device in inventory["devices"]:
        wan1 = device["uplinks"].get("wan1", {})
        wan2 = device["uplinks"].get("wan2", {})

        writer.writerow({
            "hostname": device.get("hostname", ""),
            "network": device.get("network", ""),
            "model": device.get("model", ""),
            "serial": device.get("serial", ""),

            "wan1_ip": wan1.get("ip", ""),
            "wan1_public_ip": wan1.get("public_ip", ""),
            "wan1_status": wan1.get("status", ""),

            "wan2_ip": wan2.get("ip", ""),
            "wan2_public_ip": wan2.get("public_ip", ""),
            "wan2_status": wan2.get("status", "")
        })

print(f"YAML inventory written to: {YAML_FILE}")
print(f"CSV inventory written to:  {CSV_FILE}")