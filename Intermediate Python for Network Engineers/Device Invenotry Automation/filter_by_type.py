import csv

def load_inventory(filename):
    """Load inventory from file"""
    inventory = []
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory.append(row)
        return inventory

def filter_by_type(inventory, device_type):
    """Filter inventory by device type"""
    print(f"\nDevices of type {device_type}:")
    found = False
    for device in inventory:
        if device["Device Type"] == device_type:
            print(device)
            found = True
    if not found:
        print("No devices found with that type")

inventory = load_inventory("inventory.txt")
filter_by_type(inventory, "Router")
filter_by_type(inventory, "Load Balancer")