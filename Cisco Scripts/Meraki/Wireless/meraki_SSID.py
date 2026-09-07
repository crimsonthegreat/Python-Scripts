import meraki
import csv
from datetime import datetime, timezone

API_KEY = ""
ORG_ID = ""
SSID_NAME = ""

OUTPUT_FILE = "meraki_ssid_clients_last_24h.csv"

# Initialize Meraki Dashboard SDK
dashboard = meraki.DashboardAPI(
    API_KEY,
    suppress_logging=True,
    wait_on_rate_limit=True
)

TIMESPAN_SECONDS = 86400  # 24 hours


def get_ssid_number(network_id):
    """Return SSID number for a given SSID name in a network"""
    ssids = dashboard.wireless.getNetworkWirelessSsids(network_id)
    for ssid in ssids:
        if ssid["name"] == SSID_NAME:
            return ssid["number"]
    return None


def main():
    networks = dashboard.organizations.getOrganizationNetworks(ORG_ID)

    rows = []

    for network in networks:
        network_id = network["id"]
        network_name = network["name"]

        try:
            ssid_number = get_ssid_number(network_id)
            if ssid_number is None:
                continue

            clients = dashboard.networks.getNetworkClients(
                network_id,
                timespan=TIMESPAN_SECONDS,
                perPage=1000,
                total_pages="all"
            )

            for client in clients:
                # SDK returns SSID name directly here
                if client.get("ssid") != SSID_NAME:
                    continue

                rows.append({
                    "network": network_name,
                    "ssid": SSID_NAME,
                    "client_mac": client.get("mac"),
                    "client_ip": client.get("ip"),
                    "os": client.get("os"),
                    "ap_name": client.get("recentDeviceName"),
                    "ap_serial": client.get("recentDeviceSerial"),
                    "client_description": client.get("description"),
                    "rssi": client.get("recentSignalStrength"),
                    "first_seen": client.get("firstSeen"),
                    "last_seen": client.get("lastSeen")
                })

        except Exception as e:
            print(f"Error processing network '{network_name}': {e}")

    # Write CSV
    if rows:
        with open(OUTPUT_FILE, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"CSV export complete: {OUTPUT_FILE}")
    else:
        print("No client data found.")


if __name__ == "__main__":
    main()
