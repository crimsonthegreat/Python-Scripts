# Open the file my_inventory.txt
with open("my_inventory.txt", "r") as file:
    lines = file.readlines()

print("Raw file content:")
for line in lines:
    print(line.strip())

# Initialize an empty list
inventory = []

# Iterate through each line in the file
for line in lines:
    # Split the line into fields using a comma as the delimeter
    fields = line.strip().split(',')
    device = {
        "Name": fields[0],
        "Management IP": fields[1],
        "Status": fields[2]
    } 
    inventory.append(device)

print("Full Device Inventory")
for device in inventory:
    print(device)