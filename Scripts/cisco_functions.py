import paramiko
import re
import time
import getpass
import pandas as pd
import os

def user_input():
    """Prompt user for IP address, username, and password"""
    # Prompt for IP address, username, and password
    ip = input("Enter the IP address of the switch: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return ip, username, password

def ssh_to_switch(ip, username, password):
    """Establish SSH connection to the switch and return the shell object"""
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        # Load system host keys
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {ip}...")
        # Connect to the switch
        ssh.connect(ip, username=username, password=password)
        # Create a shell object
        shell = ssh.invoke_shell()
        # Wait 1 second for the shell to be ready
        time.sleep(1)
        return shell
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")
        return None

def get_version(shell):
    """Send command to get the version of the switch"""
    try:
        print("Getting version...")
        # Send command to disable paging
        shell.send("terminal length 0\n")
        # Wait 1 second for the command to be processed
        time.sleep(1)
        # Send command to get the version
        shell.send("show version\n")
        # Wait 2 seconds for the command to be processed
        time.sleep(2)
        # Receive the output
        output = ""
        # Check if the shell has data to read
        if shell.recv_ready():
            output += shell.recv(65535).decode('utf-8')
        else:
            print("No data received from the switch.")
            return None
        # Match the version string using regex
        version_match = re.search(r'Version (\S+),?', output)
        version = version_match.group(1).strip(',')
        # Wait 1 second for the command to be processed
        time.sleep(1)
        # Print the version
        print(f"Current version is: {version}")
        return version
    except Exception as e:
        print(f"Failed to get version: {e}")

def get_mac_table(shell):
    """Send command to get the MAC address table of the switch"""
    try:
        print("Getting MAC address table...")
        # Send command to disable paging
        shell.send("terminal length 0\n")
        # Wait 1 second for the command to be processed
        time.sleep(1)
        # Send command to get the MAC address table
        shell.send("show mac address-table\n")
        # Wait 2 seconds for the command to be processed
        time.sleep(2)
        # Receive the output
        output = ""
        # Max time to wait for output
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            if shell.recv_ready():
                output += shell.recv(65535).decode('utf-8')
            # Check for switch prompt
            if re.search(r'\S+[>#]\s*$', output, re.MULTILINE):
                break
            time.sleep(0.1)
        
        #Clean up the output
        output = output.replace('\r', '')
        # Parse the Mac address table
        mac_data = []

        mac_regex = re.compile(
            r'^\s*(\d+)\s+([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+(\S+)\s+(\S+).*$', re.MULTILINE)
        
        for match in mac_regex.finditer(output):
                    mac_data.append({
                        'Vlan': match.group(1),
                        'Mac Address': match.group(2),
                        'Type': match.group(3),
                        'Ports': match.group(4)
                    })
        
        # Print the MAC address table
        if mac_data:
            print("MAC address table:")
            for entry in mac_data:
                print(f"Vlan: {entry['Vlan']}, Mac Address: {entry['Mac Address']}, Type: {entry['Type']}, Ports: {entry['Ports']}")
        else:
            print("No MAC address entries found.")

        return mac_data
        
    except Exception as e:
        print(f"Failed to get MAC address table: {e}")