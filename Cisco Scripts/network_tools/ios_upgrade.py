"""Reusable Cisco IOS-XE software upgrade functions."""

import netmiko
from netmiko.scp_functions import progress_bar


def get_ios_xe_version(ssh):
    """Return the current IOS-XE software version."""

    return ssh.send_command(
        "show version | include Cisco IOS XE Software, Version"
    )


def check_file_system(ssh, device_file, file_system):
    """Check for an image in a device filesystem."""

    return ssh.send_command(
        f"dir {file_system}:{device_file}"
    )


def copy_file(
    ssh,
    local_file,
    device_file,
    file_system
):
    """Copy an image to the device and verify the transfer."""

    result = netmiko.file_transfer(
        ssh,
        source_file=local_file,
        dest_file=device_file,
        file_system=file_system,
        direction="put",
        overwrite_file=True,
        progress4=progress_bar,
    )

    return result


def install_ios_xe(ssh, file_system, device_file):
    """Save the configuration and initiate an IOS-XE install."""

    ssh.save_config()

    command = (
        f"install add file "
        f"{file_system}:{device_file} "
        f"activate commit prompt-level none"
    )

    return ssh.send_command(
        command,
        expect_string="#",
        read_timeout=300
    )