import netmiko
import getpass
import subprocess
from netmiko.scp_functions import progress_bar
import time

def connect_info():
    # Get input from user on connection parameters
    ip = input("Please Enter IP Address: ")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    cisco = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': username,
            'password': password
        }
    
    return cisco

def get_file_system():
    # Get the file_system to check for device
    file_system = [
        "bootflash", 
        "flash",
        "usbflash0",
        "usbflash1"
        ]
    
    number = 1
    for system in file_system:
        print(f"\n{number}) {system}:")
        number += 1

    while True:
        while True:
            select_system = input("\nPlease enter the number for the file system [1-4]: ")
            try:
                select_system = int(select_system)
                break
            except ValueError:
                print("Please enter a number between 1 and 4!")
        
        if select_system == 1:
            print("\nYou have selcted bootflash")
            flash_system = file_system[0]
            break
        elif select_system == 2:
            print("\nYou have selcted flash")
            flash_system = file_system[1]
            break
        elif select_system == 3:
            print("\nYou have selcted usbflash0")
            flash_system = file_system[2]
            break
        elif select_system == 4:
            print("\nYou have selcted usbflash1")
            flash_system = file_system[3]
            break
        else:
            print("Please enter a number between 1 and 4!")

    return flash_system

def device_file_name():
    # Prompt user for the name of the file in the file system
    device_file = input("\nPlease enter the name of the file on the switch (match the Cisco Image name): ")
    return device_file
        
def copy_file(cisco, device_file, file_system):
    print("Please enter the name of the file you would like to upload to the device")
    local_file = input("(include the full path to the file excluding the filename): ")
    local_file = rf"{local_file}{device_file}"

    try:
        with netmiko.ConnectHandler(**cisco) as ssh:
            transfer_results = netmiko.file_transfer(
                ssh,
                source_file=local_file,
                dest_file=device_file,
                direction="put",
                overwrite_file=True,
                progress4=progress_bar,
            )
        
        if transfer_results.get("file_verified"):
            print(f"Success! File transferred to {file_system}.")
        else:
            print("Transfer finished, but failed to verify.")
        return device_file
    
    except Exception as e:
        print(f"An Error occurred: {e}")

def show_version_ios_xe(cisco):
    # Show version on current device

    try:
        with netmiko.ConnectHandler(**cisco) as ssh:
            version = ssh.send_command("show version | inc Cisco IOS XE Software, Version")
            print(f"{version}\n")

    except Exception as e:
        print(f"An Error occurred: {e}")

def check_file_system(cisco, device_file, file_system):
    # Check the file system files

    try:
        with netmiko.ConnectHandler(**cisco) as ssh:
            ssh.send_command('terminal length 0')
            output = ssh.send_command(f'dir {file_system}:{device_file}')
            print(f"{output}\n")

    except Exception as e:
        print(f"An Error occurred: {e}")

def update_device(cisco, file_system, device_file):
    # Send the update commands to the device

    try:
        with netmiko.ConnectHandler(**cisco) as ssh:
            print("Exceuting save and upgrade")
            ssh.send_command("wr")

            print("Executing update...")
            print("The device will reboot after execution")
            output = ssh.send_command(f"install add file {file_system}:{device_file} activate commit prompt-level none",
                                      expect_string='#')
            print("Commands sent successfully. Device is rebooting.")
            print(output)

    except Exception as e:
        print(f"An Error occurred: {e}")

def ping_device(ip, count=1, timeout=2):
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

def main():
    while True:
        cisco = connect_info()
        ip = cisco['host']
        
        file_system = get_file_system()
        device_file = device_file_name()
        
        print(f"\nChecking reachability for {ip}\n")
        if ping_device(ip, count=1, timeout=2):
            print(f"!!!!!\n{ip} is reachable\n\n")
        else:
            print(f".....\n {ip} is not reachable\n\n")
            quit()
        
        print("Current Version:")
        show_version_ios_xe(cisco)

        while True:
            print(f"Please verify the file is in the {file_system}:\n")
            check_file_system(cisco=cisco, device_file=device_file, file_system=file_system)

            print("[Enter q at any prompt to exit]")
            file_check = input(f"Is the file you expected in the {file_system}? [y/n]: ")
            file_check = file_check.lower()

            if file_check == 'n':
                while True:
                    scp_file = input("Would you like to copy the file to the device? [y/n]: ")
                    scp_file = scp_file.lower()

                    if scp_file == 'n' or scp_file == 'q':
                        quit()
                    elif scp_file =='y':
                        print("You will be asked to enter details about the file:\n")
                        copy_file(cisco=cisco, device_file=device_file, file_system=file_system)
                        break
                    else:
                        print("Please enter y or n")

            elif file_check == 'y':
                update = input("Would you like to proceed with the update? [y/n]: ")
                update = update.lower()

                if update == 'n' or update == 'q':
                    quit()
                elif update == 'y':
                    update_device(cisco=cisco, device_file=device_file, file_system=file_system)
                    print("Waiting 600 seconds for initial ping test\n")
                    time.sleep(600)

                    if ping_device(ip, count=1,timeout=2):
                        print(f"!!!!!\n {ip} is back online")
                    else:
                        print(f".....\n {ip} is still unreachable. Waiting 300 seconds for second ping test")
                        time.sleep(300)

                        if ping_device(ip, count=1,timeout=2):
                            print(f"!!!!!\n {ip} is back online")
                        else:
                            print(f".....\n {ip} is still unreachable. Please begin manual checks!")
                    
                    print("Updated Version:")
                    show_version_ios_xe(cisco)

                    break
                else:
                    print("Please enter y or n to continue...")

            elif file_check == 'q':
                quit()

            else:
                print("Please enter y or n to continue...")
        
        again = input("Would you like to connect to another device? [y/n]: ")
        again = again.lower()

        if again == 'n' or again == 'q':
            quit()
        elif again == 'y':
            print("Script will run again!")
            continue
        else:
            print("Please enter y or n to continue...")

if __name__ == "__main__":
    main()