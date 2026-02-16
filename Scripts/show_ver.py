from cisco_functions import user_input, ssh_to_switch, get_version

def main():
    ip, username, password = user_input()
    shell = ssh_to_switch(ip, username, password)
    if shell is None:
        print("Connection failed. Exiting.")
        return
    else:
        print("Connection successful")
    get_version(shell)
    # Check if the version matches the golden version
    shell.close()

if __name__ == "__main__":
    main()