import csv
import ipaddress
import re
from pathlib import Path

import yaml


SVI_PATTERN = re.compile(r"^interface\s+Vlan(\d+)\s*$", re.IGNORECASE)
HELPER_PATTERN = re.compile(
    r"^ip helper-address(?:\s+vrf\s+\S+)?\s+(\d{1,3}(?:\.\d{1,3}){3})$",
    re.IGNORECASE
)


def load_helper_addresses(file_path):
    """Load unique IPv4 helper addresses from YAML, YML, or CSV."""

    path = Path(file_path)

    if path.suffix.lower() in (".yaml", ".yml"):
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        if not isinstance(data, dict) or not isinstance(data.get("ip_helpers"), list):
            raise ValueError("YAML file must contain a top-level 'ip_helpers' list.")

        raw_addresses = data["ip_helpers"]

    elif path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or "ip_helper" not in reader.fieldnames:
                raise ValueError("CSV file must contain an 'ip_helper' column.")

            raw_addresses = [row["ip_helper"] for row in reader]
    else:
        raise ValueError("IP helper file must be CSV, YAML, or YML.")

    addresses = []

    for row_number, value in enumerate(raw_addresses, start=1):
        try:
            address = str(ipaddress.IPv4Address(str(value).strip()))
        except ipaddress.AddressValueError as error:
            raise ValueError(
                f"Invalid IP helper address at entry {row_number}: {value}"
            ) from error

        if address not in addresses:
            addresses.append(address)

    if not addresses:
        raise ValueError("The IP helper file does not contain any addresses.")

    return addresses


def get_svi_helpers(ssh):
    """Discover configured SVIs and their current non-VRF helper addresses."""

    output = ssh.send_command("show running-config | section ^interface Vlan")
    svis = {}
    current_interface = None

    for line in output.splitlines():
        stripped = line.strip()
        interface_match = SVI_PATTERN.match(stripped)

        if interface_match:
            current_interface = f"interface Vlan{interface_match.group(1)}"
            svis.setdefault(current_interface, [])
            continue

        if current_interface:
            helper_match = HELPER_PATTERN.match(stripped)

            if helper_match and " vrf " not in f" {stripped.lower()} ":
                address = str(ipaddress.IPv4Address(helper_match.group(1)))

                if address not in svis[current_interface]:
                    svis[current_interface].append(address)

    return svis


def build_helper_commands(svis, desired_helpers, mode="ensure", excluded_vlans=None):
    """Build per-SVI IOS commands for ensure, replace, or remove mode."""

    if mode not in ("ensure", "replace", "remove"):
        raise ValueError("Mode must be ensure, replace, or remove.")

    excluded = {int(vlan) for vlan in (excluded_vlans or [])}
    desired = list(dict.fromkeys(desired_helpers))
    command_sets = {}

    for interface, existing_helpers in svis.items():
        vlan_id = int(interface.lower().replace("interface vlan", ""))

        if vlan_id in excluded:
            continue

        commands = [interface]

        if mode == "replace":
            for address in existing_helpers:
                if address not in desired:
                    commands.append(f"no ip helper-address {address}")

            for address in desired:
                if address not in existing_helpers:
                    commands.append(f"ip helper-address {address}")

        elif mode == "remove":
            for address in desired:
                if address in existing_helpers:
                    commands.append(f"no ip helper-address {address}")

        else:
            for address in desired:
                if address not in existing_helpers:
                    commands.append(f"ip helper-address {address}")

        if len(commands) > 1:
            command_sets[interface] = commands

    return command_sets


def apply_helper_commands(ssh, command_sets, dry_run=False):
    """Apply prepared helper commands or return them unchanged for a dry run."""

    outputs = []

    if not dry_run:
        for commands in command_sets.values():
            outputs.append(ssh.send_config_set(commands))

    return {
        "changed": bool(command_sets) and not dry_run,
        "commands": list(command_sets.values()),
        "output": outputs
    }
