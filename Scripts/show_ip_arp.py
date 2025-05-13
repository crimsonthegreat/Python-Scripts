from cisco_functions import user_input, ssh_to_switch, get_arp
import re
import time
import getpass
import pandas as pd

def main():
    ip, username, password = user_input()
    shell = ssh_to_switch(ip, username, password)
    if shell is None:
        print("Connection failed. Exiting.")
        return
    else:
        print("Connection successful")
    
    # Get the ARP table
    get_arp(shell)
    shell.close()

if __name__ == "__main__":
    main()