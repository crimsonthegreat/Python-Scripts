#!/usr/bin/env python3

import meraki
import json
import csv
import logging
from datetime import datetime

# =====================================================
# Configuration
# =====================================================

API_KEY = ""
ORG_ID = ""

# Network tag used to identify SD-WAN sites
NETWORK_TAG = ""

# Set to False when ready to make changes
DRY_RUN = False

# New DHCP Relay Servers
NEW_RELAY_SERVERS = [
    ""
]

# =====================================================
# File Names
# =====================================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

LOG_FILE = f"meraki_dhcp_relay_{timestamp}.log"
CSV_FILE = f"dhcp_relay_changes_{timestamp}.csv"
ROLLBACK_FILE = f"rollback_dhcp_relay_{timestamp}.json"

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# =====================================================
# Dashboard Connection
# =====================================================

dashboard = meraki.DashboardAPI(
    API_KEY,
    suppress_logging=True
)

# =====================================================
# Get Networks
# =====================================================

networks = dashboard.organizations.getOrganizationNetworks(
    ORG_ID,
    total_pages='all'
)

rollback_data = []
csv_changes = []

print(f"\nMode: {'DRY RUN' if DRY_RUN else 'LIVE CHANGES'}\n")

for network in networks:

    tags = network.get("tags", [])

    if NETWORK_TAG not in tags:
        continue

    network_id = network["id"]
    network_name = network["name"]

    print(f"Processing: {network_name}")

    try:

        vlans = dashboard.appliance.getNetworkApplianceVlans(
            network_id
        )

        for vlan in vlans:

            vlan_id = vlan["id"]

            if vlan.get("dhcpHandling") != "Relay DHCP to another server":
                continue

            current_relays = vlan.get(
                "dhcpRelayServerIps",
                []
            )

            rollback_data.append({
                "networkName": network_name,
                "networkId": network_id,
                "vlanId": vlan_id,
                "vlanName": vlan["name"],
                "dhcpRelayServerIps": current_relays
            })

            csv_changes.append({
                "network": network_name,
                "vlan": vlan_id,
                "old_relays": ",".join(current_relays),
                "new_relays": ",".join(NEW_RELAY_SERVERS),
                "status": "DRY_RUN" if DRY_RUN else "UPDATED"
            })

            print(
                f"  VLAN {vlan_id}: "
                f"{current_relays} -> "
                f"{NEW_RELAY_SERVERS}"
            )

            logging.info(
                f"{network_name} VLAN {vlan_id}: "
                f"{current_relays} -> "
                f"{NEW_RELAY_SERVERS}"
            )

            if not DRY_RUN:

                dashboard.appliance.updateNetworkApplianceVlan(
                    network_id,
                    vlan_id,
                    dhcpRelayServerIps=NEW_RELAY_SERVERS
                )

    except Exception as e:

        logging.error(
            f"{network_name} failed: {str(e)}"
        )

        print(
            f"ERROR processing {network_name}: {e}"
        )

# =====================================================
# Save Rollback File
# =====================================================

with open(ROLLBACK_FILE, "w") as f:
    json.dump(
        rollback_data,
        f,
        indent=4
    )

# =====================================================
# Save CSV Report
# =====================================================

with open(CSV_FILE, "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "network",
            "vlan",
            "old_relays",
            "new_relays",
            "status"
        ]
    )

    writer.writeheader()
    writer.writerows(csv_changes)

print("\nCompleted")
print(f"Log File: {LOG_FILE}")
print(f"CSV Report: {CSV_FILE}")
print(f"Rollback File: {ROLLBACK_FILE}")