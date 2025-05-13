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

def get_interface_status(shell):
    """Send command to get the interface status of the switch"""
    try:
        print("Getting interface status...")
        # Send command to disable paging
        shell.send("terminal length 0\n")
        # Wait 1 second for the command to be processed
        time.sleep(1)
        # Send command to get the interface status
        shell.send("show interface status\n")
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
        
        lines = output.splitlines()
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # Skip empty lines, prompts, echoed commands, and header
            if (line and
                not re.match(r'^\S+[>#]', line) and  # Skip prompts (e.g., Core#)
                not re.match(r'terminal\s+length\s+0', line) and  # Skip echoed command
                not re.match(r'show\s+interface\s+status', line) and  # Skip echoed command
                not re.match(r'Port\s+Name\s+Status', line)):  # Skip header
                cleaned_lines.append(line)

        # Parse the interface status
        int_data = []
        
        int_regex = re.compile(
            r'^([A-Za-z]+\d+(?:/\d+)?(?:,\s*)?)\s+([^\s]*(?:\s+[^\s]+)*)?\s+(connected|notconnect|disabled|err-disabled|suspended)\s+(\S+)\s+(a-full|full|half|a-half|auto)\s+(a-\d+|auto|\d+)\s+(\S+)\s*$'
        )

        for line in cleaned_lines:
            match = int_regex.match(line)
            if match:
                int_data.append({
                    'Port': match.group(1).rstrip(',').strip(),  # Remove trailing comma
                    'Name': match.group(2) or '',  # Handle None as empty string
                    'Status': match.group(3),
                    'Vlan': match.group(4),
                    'Duplex': match.group(5),
                    'Speed': match.group(6),
                    'Type': match.group(7).strip()
                })
            else:
                print(f"Failed to parse line: {line}")  # Log unmatched lines
        
        # Print the interface status
        if int_data:
            print("Interface status:")
            for entry in int_data:
                print(f"Port: {entry['Port']}, Name: {entry['Name']}, Status: {entry['Status']}, Vlan: {entry['Vlan']}, Duplex: {entry['Duplex']}, Speed: {entry['Speed']}, Type: {entry['Type']}")
        else:
            print("No interface entries found.")

        return int_data
        
    except Exception as e:
        print(f"Failed to get interface status: {e}")

def get_arp(shell):
    """Send command to get the ARP table of the switch"""
    try:
        print("Getting ARP table...")
        # Send command to disable paging
        shell.send("terminal length 0\n")
        # Wait 1 second for the command to be processed
        time.sleep(1)
        # Send command to get the ARP table
        shell.send("show ip arp\n")
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

        lines = output.splitlines()
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # Skip empty lines, prompts, echoed commands, and header
            if (line and
                not re.match(r'^\S+[>#]', line) and  # Skip prompts (e.g., Core#)
                not re.match(r'terminal\s+length\s+0', line) and  # Skip echoed command
                not re.match(r'show\s+ip\s+arp', line) and  # Skip echoed command
                not re.match(r'Protocol\s+Address\s+Age\s+\(min\)\s+Hardware\s+Addr\s+Type\s+Interface', line)):  # Skip header
                cleaned_lines.append(line)
        # Parse the ARP table
        arp_data = []
        
        arp_regex = re.compile(
            r'^\s*(\S+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+|-)\s+([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}|[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})\s+(\S+)\s+(\S+)\s*$'
        )

        for line in cleaned_lines:
            match = arp_regex.match(line)
            if match:
                arp_data.append({
                    'Protocol': match.group(1),
                    'Address': match.group(2),
                    'Age': match.group(3),
                    'Hardware Address': match.group(4),
                    'Type': match.group(5),
                    'Interface': match.group(6),
                })

        # Print the ARP table       
        if arp_data:
            print("ARP table:")
            for entry in arp_data:
                print(f"Protocol: {entry['Protocol']}, Address: {entry['Address']}, Age: {entry['Age']}, Hardware Address: {entry['Hardware Address']}, Type: {entry['Type']}, Interface: {entry['Interface']}")
        else:
            print("No ARP entries found.")
        return arp_data
    
    except Exception as e:
        print(f"Failed to get ARP table: {e}")