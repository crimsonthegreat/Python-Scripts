from cisco_functions import user_input, ssh_to_switch, get_interface_status

def main():
    ip, username, password = user_input()
    shell = ssh_to_switch(ip, username, password)
    if shell is None:
        print("Connection failed. Exiting.")
        return
    else:
        print("Connection successful")
    
    # Get the interface status
    get_interface_status(shell)
    shell.close()

if __name__ == "__main__":
    main()