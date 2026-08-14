import netmiko
import base_functions as bf
import acl_functions as acl

print("\n" + "=" * 60)
print("Remove ACL from VTY lines" + "\n" + "=" * 60)


def process_device(device, username, password, acl_name):
    """Process one device using one SSH connection."""

    ip = device["ip"]

    print("\n" + "=" * 60)
    print(f"Processing Device: {ip}")
    print("=" * 60)

    print(f"\nChecking reachability for {ip}...")

    if not acl.ping_device(ip):

        print(f"{ip} is not reachable.")

        return {
            "ip": ip,
            "status": "failed",
            "reason": "Ping failed"
        }

    print(f"{ip} is reachable.")

    cisco = bf.build_connection(
        device=device,
        username=username,
        password=password
    )

    try:

        # ONE SSH CONNECTION FOR THE ENTIRE DEVICE
        with netmiko.ConnectHandler(**cisco) as ssh:

            hostname = ssh.find_prompt().replace(
                "#",
                ""
            ).replace(
                ">",
                ""
            )

            print(f"Connected to {hostname} ({ip})")

            print("Showing existing VTY line configuration")

            acl_reference = acl.get_vty_acl_references(ssh=ssh, acl_name=acl_name)

            print(acl_reference)

            bf.user_input("\nWould you like to remove the ACL from the VTY line? [y/n]: ")

            acl.remove_vty_acl_references(ssh=ssh, references=acl_reference)

            # Save
            print("\nSaving configuration...")

            save_output = bf.save_config(ssh=ssh)

            print(save_output)

            return {
                "ip": ip,
                "hostname": hostname,
                "status": "success",
                "reason": ""
            }

    except netmiko.NetmikoAuthenticationException:

        print(
            f"Authentication failed for {ip}."
        )

        return {
            "ip": ip,
            "status": "failed",
            "reason": "Authentication failure"
        }

    except netmiko.NetmikoTimeoutException:

        print(
            f"Connection to {ip} timed out."
        )

        return {
            "ip": ip,
            "status": "failed",
            "reason": "Connection timeout"
        }

    except Exception as e:

        print(
            f"Unexpected error on {ip}: {e}"
        )

        return {
            "ip": ip,
            "status": "failed",
            "reason": str(e)
        }
    
def main():

    args = bf.get_arguments()

    username,password = bf.get_credentials()

    devices = bf.get_devices(inventory_file=args.inventory_file)

    if not devices:
        print("No valid devices to process.")
        return

    print(f"\n{len(devices)} device(s) selected:")

    for device in devices:
        print(f"  {device['ip']}")

    