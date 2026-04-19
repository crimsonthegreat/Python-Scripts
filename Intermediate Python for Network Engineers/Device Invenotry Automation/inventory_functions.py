import csv

def load_inventory(filename):
    """
    Load device inventory data from a CSV file into a list of dictionaries.
    """
    inventory = []
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory.append(row)
    return inventory

def save_inventory(filename, inventory):
    """
    Save device inventory data to a CSV File
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Management IP", "Device Type", "Status"])
        writer.writeheader()
        writer.writerows(inventory)
    print(f"Inventory saved to {filename}")

def display_inventory(inventory):
    """
    Display device inventory data in a user-friendly format.
    """
    print("\nDevice Inventory:")
    for device in inventory:
        print(f"Name: {device['Name']}, IP: {device['Management IP']}, Device Type: {device['Device Type']}"
              f"Status: {device['Status']}")
        
def filter_devices(inventory, status):
    """
    Filter devices based on their status.
    """
    filtered_devices = [device for device in inventory if device["Status"] == status]
    return filtered_devices

# Load inventory
inventory = load_inventory("inventory.txt")
print("Loading inventory:")
for device in inventory:
    print(device)

# Display inventory
display_inventory(inventory)

# Filter and display online devices
online_devices = filter_devices(inventory, "Online")
print("\nOnline Devices:")
for device in online_devices:
    print(device)

# Save inventory to a new file
save_inventory("updated_inventory.csv", inventory)


