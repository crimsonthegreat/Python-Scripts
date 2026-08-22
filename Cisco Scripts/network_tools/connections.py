import subprocess

def build_connection_param(device, username, password):
    """Build Netmiko connection dictionary."""

    return {
        "device_type": device.get(
            "device_type",
            "cisco_ios"
        ),
        "ip": device["ip"],
        "username": username,
        "password": password
    }

def ping_device(ip, count=1, timeout=2):
    """Ping a device."""

    cmd = [
        "ping",
        "-c", str(count),
        "-W", str(timeout),
        ip
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=(count * timeout) + 2
        )

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        return False

    except Exception as e:
        print(f"Ping failed: {e}")
        return False

def save_config(ssh):
    """Function to save the configuration"""

    return ssh.save_config()

def get_hostname(ssh):
    """Return hostname from the device prompt."""

    return (
        ssh.find_prompt()
        .strip()
        .rstrip("#>")
    )