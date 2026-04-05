import csv

# Updated inventory data
inventory = [
    {
        "Name" : "Router1",
        "Management IP" : "10.10.10.1",
        "Device Type" : "Router",
        "Status" : "Online"
    },
    {
        "Name" : "Router2",
        "Management IP" : "10.10.20.1",
        "Device Type" : "Router",
        "Status" : "Online"
    },
    {
        "Name" : "Switch1",
        "Management IP" : "10.10.10.11",
        "Device Type" : "Switch",
        "Status" : "Online"
    },
    {
        "Name" : "Switch2",
        "Management IP" : "10.10.20.11",
        "Device Type" : "Switch",
        "Status" : "Offline"
    }
]

for device in inventory:
    if device["Status"] == "Offline":
        device["Status"] = "Online"

# Define the CSV file name
filename = "updated_inventory.csv"

# Open the file in write mode
with open(filename, mode="w", newline="") as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["Name", "Management IP", "Device Type", "Status"])

    # Write each device's data as a row
    for device in inventory:
        writer.writerow([device["Name"], device["Management IP"], device["Device Type"], device["Status"]])

print(f"Inventory saved to {filename}")