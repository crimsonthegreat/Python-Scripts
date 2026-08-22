#!/usr/bin/env python3

import time
from pathlib import Path

import netmiko
import network_tools


def get_file_system():
    """Prompt user for target device filesystem."""

    file_systems = [
        "bootflash",
        "flash",
        "usbflash0",
        "usbflash1",
    ]

    for number, file_system in enumerate(file_systems, start=1):
        print(f"{number}) {file_system}")

    while True:
        try:
            selection = int(
                input(
                    "\nPlease select the file system [1-4]: "
                )
            )

            if 1 <= selection <= len(file_systems):
                return file_systems[selection - 1]

        except ValueError:
            pass

        print("Please enter a number between 1 and 4.")


def get_image_file():
    """Get local IOS-XE image and device filename."""

    local_file = Path(
        input(
            "\nEnter the full path to the IOS-XE image: "
        ).strip()
    )

    return local_file, local_file.name


def wait_for_device(ip):
    """Wait for device to return after upgrade."""

    print("\nWaiting 600 seconds for initial ping test...")
    time.sleep(600)

    if network_tools.ping_device(ip):
        print(f"{ip} is back online.")
        return True

    print(
        f"{ip} is still unreachable. "
        "Waiting another 300 seconds..."
    )

    time.sleep(300)

    if network_tools.ping_device(ip):
        print(f"{ip} is back online.")
        return True

    print(
        f"{ip} is still unreachable. "
        "Please begin manual checks."
    )

    return False


def process_device(device, username, password):

    ip = device["ip"]

    if not network_tools.ping_device(ip):
        print(f"{ip} is not reachable.")
        return

    connection_params = network_tools.build_connection(
        device,
        username,
        password,
    )

    file_system = get_file_system()
    local_file, device_file = get_image_file()

    try:
        with netmiko.ConnectHandler(**connection_params) as ssh:

            hostname = (
                ssh.find_prompt()
                .strip()
                .rstrip("#>")
            )

            print(f"\nConnected to {hostname} ({ip})")

            # Current version
            print("\nCurrent Version:")

            print(
                network_tools.get_ios_xe_version(ssh)
            )

            # Check image
            print(
                f"\nChecking {file_system} "
                f"for {device_file}..."
            )

            file_output = network_tools.check_file_system(
                ssh,
                device_file,
                file_system,
            )

            print(file_output)

            file_exists = input(
                "\nIs the expected image already present? [y/n]: "
            ).lower().strip()

            if file_exists in ("n", "no"):

                copy_image = input(
                    "Copy image to device? [y/n]: "
                ).lower().strip()

                if copy_image not in ("y", "yes"):
                    return

                print("\nCopying image...")

                transfer_result = network_tools.copy_file(
                    ssh,
                    str(local_file),
                    device_file,
                    file_system,
                )

                if not transfer_result.get("file_verified"):
                    print("ERROR: File failed verification.")
                    return

                print("Image successfully transferred and verified.")

            # Confirmation
            proceed = input(
                "\nProceed with IOS-XE upgrade? [y/n]: "
            ).lower().strip()

            if proceed not in ("y", "yes"):
                return

            print("\nStarting IOS-XE installation...")

            output = network_tools.install_ios_xe(
                ssh,
                file_system,
                device_file,
            )

            print(output)

    except netmiko.NetmikoAuthenticationException:
        print(f"Authentication failed for {ip}.")
        return

    except netmiko.NetmikoTimeoutException:
        # A timeout/disconnect can be expected during reboot.
        print(
            f"Connection to {ip} closed/timed out "
            "during the upgrade."
        )

    except Exception as error:
        print(f"Upgrade error on {ip}: {error}")
        return

    # Device should now be rebooting
    if not wait_for_device(ip):
        return

    # Reconnect after reboot
    try:
        with netmiko.ConnectHandler(**connection_params) as ssh:

            print("\nUpdated Version:")

            print(
                network_tools.get_ios_xe_version(ssh)
            )

    except Exception as error:
        print(
            f"Device responded to ping but SSH "
            f"reconnection failed: {error}"
        )


def main():

    username, password = network_tools.get_credentials()

    while True:

        devices = network_tools.get_devices()

        if not devices:
            return

        process_device(
            devices[0],
            username,
            password,
        )

        again = input(
            "\nUpgrade another device? [y/n]: "
        ).lower().strip()

        if again not in ("y", "yes"):
            break


if __name__ == "__main__":
    main()