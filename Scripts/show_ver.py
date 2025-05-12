import paramiko
import re
import time
import getpass


def user_input():
    """Prompt user for IP address, username, and password"""
    # Prompt for IP address, username, and password
    ip = input("Enter the IP address of the switch: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    # Prompt for the version of the golden image
    golden_version = input("Enter the version of the golden image: ")
    return ip, username, password, golden_version

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

def main():
    ip, username, password, golden_version = user_input()
    shell = ssh_to_switch(ip, username, password)
    if shell is None:
        print("Connection failed. Exiting.")
        return
    else:
        print("Connection successful")
    version = get_version(shell)
    # Check if the version matches the golden version
    if version == golden_version:
        print("This device is up to date")
    else:
        print("Update this device")
    shell.close()

if __name__ == "__main__":
    main()