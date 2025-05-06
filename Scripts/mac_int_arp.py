import paramiko
import time
import re
import pandas as pd
import os
import getpass

def execute_command(shell, command, timeout=2):
    """Execute command and handle pagination"""
    shell.send(f"{command}\n")
    time.sleep(timeout)
    
    output = ""
    while True:
        data = shell.recv(65535).decode('utf-8')
        output += data
        
        # Check for pagination prompt
        if "--More--" in data:
            shell.send(" ")  # Send space to get next page
            time.sleep(0.5)
        else:
            break
    
    return output.splitlines()

def get_mac_address_table(shell):
    output = execute_command(shell, "show mac address-table")
    mac_data = []
    for line in output:
        if re.match(r'^\s*\d+\s+\S+\s+\S+\s+\S+', line):
            fields = line.split()
            if len(fields) >= 4:
                mac_data.append({
                    'Vlan': fields[0],
                    'Mac Address': fields[1],
                    'Type': fields[2],
                    'Interfaces': fields[3]
                })
    return mac_data

def get_interface_status(shell):
    output = execute_command(shell, "show interface status")
    int_data = []

    for line in output:
        if line.strip().startswith("Port") or line.strip().startswith("-----") or not line.strip():
            continue

        match = re.match(r'^(\S+)\s+(\S*)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*)', line)
        if match:
            int_data.append({
                'Port': match.group(1),
                'Name': match.group(2),
                'Status': match.group(3),
                'Vlan': match.group(4),
                'Duplex': match.group(5),
                'Speed': match.group(6),
                'Type': match.group(7).strip()
            })
    return int_data

def get_ip_arp_table(shell):
    output = execute_command(shell, "show ip arp")
    arp_data = []

    for line in output:
        if line.strip().startswith("Protocol") or not line.strip():
            continue

        fields = line.split()
        if len(fields) >= 6 and re.match(r'\d+\.\d+\.\d+\.\d+', fields[1]):
            arp_data.append({
                'Protocol': fields[0],
                'Address': fields[1],
                'Age': fields[2],
                'Hardware Addr': fields[3],
                'Type': fields[4],
                'Interface': fields[5]
            })
    return arp_data

def ssh_to_switch(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {ip}...")
        ssh.connect(ip, username=username, password=password, look_for_keys=False)
        shell = ssh.invoke_shell()
        time.sleep(1)

        # Disable pagination on Cisco device
        shell.send("terminal length 0\n")
        time.sleep(1)
        shell.recv(65535)  # Clear buffer

        # Get hostname
        shell.send("sh hostname\n")
        time.sleep(1)
        output = shell.recv(65535).decode('utf-8')
        hostname = re.search(r'(\S+)#', output)
        hostname = hostname.group(1) if hostname else f"switch_{ip}"

        # Collect data
        mac_data = get_mac_address_table(shell)
        int_data = get_interface_status(shell)
        arp_data = get_ip_arp_table(shell)

        # Create output directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_dir = os.path.join(script_dir, "XLSX")
        os.makedirs(csv_dir, exist_ok=True)

        # Write to Excel
        output_file = os.path.join(csv_dir, f"{hostname}_switch_data.xlsx")
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            if mac_data:
                pd.DataFrame(mac_data).to_excel(writer, sheet_name='MAC Address Table', index=False)
            if int_data:
                pd.DataFrame(int_data).to_excel(writer, sheet_name='Interface Status', index=False)
            if arp_data:
                pd.DataFrame(arp_data).to_excel(writer, sheet_name='IP ARP', index=False)

        print(f"Data successfully saved to {output_file} with separate sheets")
        ssh.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    ip = input("Enter switch IP address: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    ssh_to_switch(ip, username, password)

if __name__ == "__main__":
    main()