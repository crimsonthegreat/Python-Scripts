def set_enable_secret(ssh, new_secret):
    """Configure the enable secret using scrypt."""

    commands = [
        f"enable algorithm-type scrypt secret {new_secret}"
    ]

    return ssh.send_config_set(commands)

def set_user_secret(ssh, username, new_secret):
    """
    Configure a privilege 15 local user
    with an scrypt-protected secret.
    """

    commands = [
        (
            f"username {username} privilege 15 "
            f"algorithm-type scrypt secret {new_secret}"
        )
    ]

    return ssh.send_config_set(commands)

def set_device_passwords(
    ssh,
    enable_secret=None,
    username=None,
    user_secret=None,
):
    """
    Update enable and/or local-user secrets using scrypt.

    Local users are configured at privilege level 15.
    """

    commands = []

    if enable_secret:
        commands.append(
            f"enable algorithm-type scrypt secret {enable_secret}"
        )

    if username and user_secret:
        commands.append(
            f"username {username} privilege 15 "
            f"algorithm-type scrypt secret {user_secret}"
        )

    if not commands:
        return ""

    return ssh.send_config_set(commands)

def verify_password_configuration(
    ssh,
    username=None,
    verify_enable=False,
):
    """
    Verify local-user and enable-secret configuration.

    User requirements:
      - privilege 15
      - Type 9 secret

    Enable requirements:
      - Type 9 secret
    """

    results = {
        "valid": True,
        "user_valid": None,
        "enable_valid": None,
    }

    if username:
        user_output = ssh.send_command(
            f"show running-config | include ^username {username} "
        )

        privilege_ok = "privilege 15" in user_output
        scrypt_ok = "secret 9" in user_output

        results["user_valid"] = (
            privilege_ok and scrypt_ok
        )

        if not results["user_valid"]:
            results["valid"] = False

    if verify_enable:
        enable_output = ssh.send_command(
            "show running-config | include ^enable secret"
        )

        results["enable_valid"] = (
            "secret 9" in enable_output
        )

        if not results["enable_valid"]:
            results["valid"] = False

    return results