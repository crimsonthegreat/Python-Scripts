"""
Reusable network automation tools.

Modules include inventory handling, device connections,
Cisco IOS configuration, Meraki API functions, and output utilities.
"""

# Credentials
from .credentials import (
    get_credentials,
)

# Inventory
from .inventory import (
    get_devices,
    load_csv_devices,
    load_yaml_devices,
    filter_devices_by_site,
)

# Connections
from .connections import (
    build_connection,
    ping_device,
    save_config,
    get_hostname,
)

# Prompts
from .prompts import (
    user_input,
)

# ACL
from .acl import (
    get_acl_type,
    get_acl_name,
    show_acl_running,
    find_terminal_deny,
    remove_terminal_deny,
    check_acl,
    get_acl_address,
    get_port,
    get_port_statement,
    get_acl_config,
    configure_acl,
    get_vty_acl_references,
    get_vty_lines,
    remove_vty_acl_references,
    restore_vty_acl_references,
    apply_acl_to_all_vty_lines,
    remove_acl,
    add_vty_acl_references,
)

# ACL Importer
from .acl_importer import (
    ACLRule,
    load_acl_rules,
    build_acl_command_sets,
    apply_acl_rules,
    normalize_address,
)

# IP Helpers
from .ip_helpers import (
    load_helper_addresses,
    get_svi_helpers,
    build_helper_commands,
    apply_helper_commands,
)

# IOS Upgrade
from .ios_upgrade import (
    get_ios_xe_version,
    check_file_system,
    copy_file,
    install_ios_xe,
)


__all__ = [
    # Credentials
    "get_credentials",

    # Inventory
    "get_devices",
    "load_csv_devices",
    "load_yaml_devices",
    "filter_devices_by_site",
    
    # Connections
    "build_connection",
    "ping_device",
    "save_config",
    "get_hostname",

    # Prompts
    "user_input",

    # ACL
    "get_acl_type",
    "get_acl_name",
    "show_acl_running",
    "find_terminal_deny",
    "remove_terminal_deny",
    "check_acl",
    "get_acl_address",
    "get_port",
    "get_port_statement",
    "get_acl_config",
    "configure_acl",
    "get_vty_acl_references",
    "get_vty_lines",
    "remove_vty_acl_references",
    "restore_vty_acl_references",
    "apply_acl_to_all_vty_lines",
    "remove_acl",
    "add_vty_acl_references",

    # ACL Importer
    "ACLRule",
    "load_acl_rules",
    "build_acl_command_sets",
    "apply_acl_rules",
    "normalize_address",

    # IP Helpers
    "load_helper_addresses",
    "get_svi_helpers",
    "build_helper_commands",
    "apply_helper_commands",

    # IOS-XE upgrades
    "get_ios_xe_version",
    "check_file_system",
    "copy_file",
    "install_ios_xe",
]

__version__ = "0.1.0"