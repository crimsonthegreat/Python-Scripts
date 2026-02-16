from cisco_functions import get_mac_table, user_input, ssh_to_switch

def main():
    ip, username, password = user_input()
    shell = ssh_to_switch(ip, username, password)
    if shell is None:
        print("Connection failed. Exiting.")
        return
    else:
        print("Connection successful")
    
    # Get the MAC address table
    get_mac_table(shell)
    shell.close()

if __name__ == "__main__":
    main()