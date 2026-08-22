import getpass

def get_credentials():
    """Get credentials once for all devices."""

    username = input("Enter Username: ").strip()
    password = getpass.getpass("Enter Password: ")

    return username, password