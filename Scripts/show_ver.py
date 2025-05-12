import paramiko
import re
import time
import getpass


def user_input():
    """Prompt user for IP address, username, and password"""
    ip = input("Enter the IP address of the switch: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    golden_version = input("Enter the version of the golden image: ")
    return ip, username, password, golden_version

def ssh_to_switch(ip, username, password):
    """Establish SSH connection to the switch and return the shell object"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {ip}...")
        ssh.connect(ip, username=username, password=password)
        shell = ssh.invoke_shell()
        time.sleep(1)
        return shell
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")
        return None

def get_version(shell):
    """Send command to get the version of the switch"""
    try:
        print("Getting version...")
        shell.send("terminal length 0\n")
        time.sleep(1)
        shell.send("show version\n")
        time.sleep(2)
        output = ""
        if shell.recv_ready():
            output += shell.recv(65535).decode('utf-8')
        else:
            print("No data received from the switch.")
            return None
        version_match = re.search(r'Version (\S+),?', output)
        version = version_match.group(1).strip(',')
        time.sleep(1)
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
    if version == golden_version:
        print("This device is up to date")
    else:
        print("Update this device")
    shell.close()

if __name__ == "__main__":
    main()