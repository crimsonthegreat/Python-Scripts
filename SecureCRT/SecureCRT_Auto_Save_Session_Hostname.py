# $language = "Python3"
# $interface = "1.0"

"""
SecureCRT: discover a Cisco or Linux hostname and save an IP-based session.

Recommended setup
-----------------
1. Edit SESSION_FOLDER below if desired. Use an empty string to save sessions
   at the root of Session Manager.
2. In SecureCRT, open Options > Edit Default Session > Connection > Logon
   Actions, enable "Run script", and select this file.
3. Connect to a previously unknown device with Quick Connect and its IP address.

After authentication, the script queries the Cisco hostname and creates a saved
Session Manager entry while retaining the IP address as the SSH destination.

The script operates on either an unsaved Quick Connect session (path "Default")
or an IP-named session that SecureCRT created because "Save session" was checked
in Quick Connect. Hostname-named saved sessions are ignored on later connects.

Supported targets:
- Cisco IOS, IOS-XE, NX-OS, and ASA devices whose CLI accepts
  "show running-config | include ^hostname" from the authenticated EXEC level.
- Linux systems with a POSIX-style shell and the "hostname" command.
"""

import datetime
import json
import os
import re
import shutil


# ---------------------------- User settings ----------------------------

# Session Manager folder in which discovered sessions will be saved.
# SecureCRT creates the folder when the session is saved.
SESSION_FOLDER = "Network Devices\\Discovered"

# True produces names such as "AUG-CORE-01 [10.20.30.40]". This prevents one
# device from overwriting another if duplicate Cisco hostnames exist.
# False produces only "AUG-CORE-01" and may overwrite an existing entry with
# the same name, depending on SecureCRT's version and settings.
INCLUDE_IP_IN_SESSION_NAME = True

# Change to False after testing if you do not want success notifications.
SHOW_SUCCESS_MESSAGE = False

# Maximum time to wait for CLI output.
COMMAND_TIMEOUT_SECONDS = 15

# Stale entries are backed up before deferred deletion.
CLEANUP_QUEUE_FILE = "AutoSaveSessionCleanup.json"
CLEANUP_BACKUP_FOLDER = "AutoSaveSessionBackups"


# Settings copied from the active Quick Connect configuration when available.
# Options that do not apply to the selected protocol are skipped safely.
ACTIVE_OPTIONS_TO_COPY = (
    "Protocol Name",
    "Hostname",
    "Port",
    "Username",
    "Credential Title",
    "Firewall Name",
    "Emulation",
    "Color Scheme",
    "ANSI Color Palette",
    "Scrollback",
    "Rows",
    "Cols",
    "Use Global Host Key Algorithms",
    "Use Global Public Key Algorithms",
    "Use Global Key Exchange Algorithms",
    "Use Global MAC",
    "Use Global Ciphers",
)


def show_error(message):
    """Display a concise error without exposing credentials or configuration."""
    crt.Dialog.MessageBox(message, "Auto-save SecureCRT session", 0x10)


def clean_terminal_text(value):
    """Remove ANSI escape sequences and terminal control characters."""
    value = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", value)
    value = value.replace("\r", "")
    return value


def sanitize_session_component(value):
    """Make a hostname safe for a SecureCRT session/file name."""
    value = value.strip()
    value = re.sub(r'[\\/:*?"<>|]', "_", value)
    value = re.sub(r"\s+", "_", value)
    value = value.rstrip(". ")
    return value


def get_prompt(screen):
    """Ask the device to redraw its prompt and return the visible prompt."""
    screen.Send("\r")
    if not screen.WaitForCursor(COMMAND_TIMEOUT_SECONDS):
        return ""

    # Give SecureCRT a short opportunity to receive the remainder of the line.
    screen.WaitForCursor(1)
    row = screen.CurrentRow
    column = screen.CurrentColumn
    if column <= 1:
        return ""

    prompt = screen.Get(row, 1, row, column - 1)
    return clean_terminal_text(prompt).strip()


def run_command(screen, command, prompt):
    """Send a command, consume its terminal echo, and return its output."""
    screen.Send(command + "\r")

    # In synchronous mode, the previously discovered prompt can still be in
    # SecureCRT's receive buffer. Waiting for the command echo consumes that
    # stale prompt and positions ReadString immediately before command output.
    if not screen.WaitForString(command, COMMAND_TIMEOUT_SECONDS):
        return ""

    return clean_terminal_text(
        screen.ReadString(prompt, COMMAND_TIMEOUT_SECONDS)
    )


def discover_cisco_hostname(screen, prompt):
    """Query and parse a configured Cisco hostname."""
    command = "show running-config | include ^hostname"
    output = run_command(screen, command, prompt)

    for line in output.split("\n"):
        match = re.match(r"^\s*hostname\s+(\S+)\s*$", line, re.IGNORECASE)
        if match:
            return sanitize_session_component(match.group(1))

    return ""


def discover_linux_hostname(screen):
    """Read Linux hostname output without depending on the shell prompt."""
    command = "hostname -s"
    screen.Send(command + "\r")

    # Consume everything through the echoed command. This also clears any old
    # prompt text left in SecureCRT's synchronous receive buffer.
    if not screen.WaitForString(command, COMMAND_TIMEOUT_SECONDS):
        return ""

    # The first newline completes the echoed command. One of the following
    # lines contains the hostname. Reading by line avoids matching a colored,
    # multi-line, or otherwise customized shell prompt.
    for _ in range(6):
        line = screen.ReadString("\n", COMMAND_TIMEOUT_SECONDS)
        candidate = clean_terminal_text(line).strip()
        if re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", candidate):
            return sanitize_session_component(candidate)

    return ""


def discover_hostname(screen, prompt):
    """Select the most likely discovery method and fall back safely."""
    prompt_terminator = prompt[-1:]

    # Non-root Linux shells normally end in $ or %. Trying Linux first avoids
    # sending a Cisco command to the shell and waiting for a timeout.
    if prompt_terminator in ("$", "%"):
        return discover_linux_hostname(screen)

    # Cisco privileged prompts and Linux root prompts both commonly end in #.
    # Try Cisco first, then use the Linux hostname command as a fallback.
    hostname = discover_cisco_hostname(screen, prompt)
    if hostname:
        return hostname

    if prompt_terminator == "#":
        return discover_linux_hostname(screen)

    return ""


def copy_active_options(source, destination):
    """Copy useful, non-secret options from the active ad-hoc configuration."""
    # Protocol must be set first because it controls which options are valid.
    try:
        destination.SetOption("Protocol Name", source.GetOption("Protocol Name"))
    except Exception:
        pass

    for option_name in ACTIVE_OPTIONS_TO_COPY:
        if option_name == "Protocol Name":
            continue
        try:
            destination.SetOption(option_name, source.GetOption(option_name))
        except Exception:
            # SecureCRT option names vary slightly by version and protocol.
            continue


def build_session_path(hostname, address, folder=None):
    """Return the desired Session Manager path."""
    if INCLUDE_IP_IN_SESSION_NAME and address:
        session_name = "{} [{}]".format(hostname, address)
    else:
        session_name = hostname

    target_folder = SESSION_FOLDER if folder is None else folder
    if target_folder:
        return target_folder.strip("\\/") + "\\" + session_name
    return session_name


def is_ip_named_session(session_path, configured_address, remote_address):
    """Return True when SecureCRT appears to have auto-saved the session by IP."""
    if session_path.lower() == "default":
        return True

    leaf_name = re.split(r"[\\/]", session_path)[-1].strip()
    possible_addresses = (configured_address, remote_address)
    return any(address and leaf_name == address.strip() for address in possible_addresses)


def get_config_path():
    """Resolve ${VDS_CONFIG_PATH} using SecureCRT's documented substitution."""
    option = "Upload Directory V2"
    config = crt.OpenSessionConfiguration("Default")
    original = config.GetOption(option)
    try:
        config.SetOption(option, "${VDS_CONFIG_PATH}")
        config.Save()
        resolved = crt.OpenSessionConfiguration("Default").GetOption(option)
    finally:
        restore = crt.OpenSessionConfiguration("Default")
        restore.SetOption(option, original)
        restore.Save()
    return resolved


def session_file(config_path, session_path):
    """Resolve and validate a Session Manager path beneath Config/Sessions."""
    sessions_root = os.path.abspath(os.path.join(config_path, "Sessions"))
    relative = session_path.replace("\\", os.sep).replace("/", os.sep) + ".ini"
    candidate = os.path.abspath(os.path.join(sessions_root, relative))
    if os.path.commonpath((sessions_root, candidate)) != sessions_root:
        raise ValueError("Session path escaped the SecureCRT Sessions folder")
    return candidate


def read_queue(queue_file):
    if not os.path.isfile(queue_file):
        return []
    try:
        with open(queue_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def write_queue(queue_file, entries):
    temp_file = queue_file + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
    os.replace(temp_file, queue_file)


def process_deferred_cleanup(config_path, current_path):
    """Delete stale, inactive entries only after verifying their replacements."""
    queue_file = os.path.join(config_path, CLEANUP_QUEUE_FILE)
    remaining = []
    for entry in read_queue(queue_file):
        old_path = entry.get("old_path", "")
        new_path = entry.get("new_path", "")
        try:
            old_file = session_file(config_path, old_path)
            new_file = session_file(config_path, new_path)
            if old_path == current_path or not os.path.isfile(new_file):
                remaining.append(entry)
                continue
            if os.path.isfile(old_file):
                backup_root = os.path.join(config_path, CLEANUP_BACKUP_FOLDER)
                stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                backup_file = os.path.join(backup_root, stamp, old_path.replace("\\", os.sep) + ".ini")
                os.makedirs(os.path.dirname(backup_file), exist_ok=True)
                shutil.copy2(old_file, backup_file)
                os.remove(old_file)
        except Exception:
            remaining.append(entry)
    write_queue(queue_file, remaining)


def queue_cleanup(config_path, old_path, new_path):
    if not old_path or old_path.lower() == "default" or old_path == new_path:
        return
    queue_file = os.path.join(config_path, CLEANUP_QUEUE_FILE)
    entries = [item for item in read_queue(queue_file) if item.get("old_path") != old_path]
    entries.append({"old_path": old_path, "new_path": new_path})
    write_queue(queue_file, entries)


def queue_stale_sessions_for_address(config_path, address, new_path):
    """Use VanDyke's documented recursive .ini iteration pattern."""
    managed_root = os.path.join(config_path, "Sessions")
    if not os.path.isdir(managed_root):
        return
    sessions_root = os.path.join(config_path, "Sessions") + os.sep
    for root, _, files in os.walk(managed_root):
        for name in files:
            base, extension = os.path.splitext(name)
            if extension.lower() != ".ini" or base in ("Default", "__FolderData__"):
                continue
            file_path = os.path.join(root, name)
            old_path = os.path.splitext(file_path.replace(sessions_root, "", 1))[0]
            old_path = old_path.replace(os.sep, "\\")
            if old_path.lower() == new_path.lower():
                continue
            try:
                old_config = crt.OpenSessionConfiguration(old_path)
                if old_config.GetOption("Hostname").strip() == address.strip():
                    queue_cleanup(config_path, old_path, new_path)
            except Exception:
                continue


def is_managed_session(path, configured_address, remote_address):
    """All saved Session Manager entries and ad-hoc sessions are managed."""
    return bool(path)


def session_parent(path):
    """Return the Session Manager folder containing a saved session."""
    normalized = path.replace("/", "\\")
    parts = normalized.split("\\")
    return "\\".join(parts[:-1])


def main():
    if not crt.Session.Connected:
        show_error("No connected session is active.")
        return

    current_path = crt.Session.Path
    config_path = get_config_path()
    process_deferred_cleanup(config_path, current_path)

    screen = crt.Screen
    previous_synchronous = screen.Synchronous
    screen.Synchronous = True

    try:
        prompt = get_prompt(screen)
        if prompt and prompt[-1:] in ("#", ">", "$", "%"):
            hostname = discover_hostname(screen, prompt)
        else:
            # Linux prompts may contain colors, span multiple lines, end in an
            # unusual character, or not be fully drawn when a logon script
            # starts. Marker-based discovery does not require prompt matching.
            hostname = discover_linux_hostname(screen)
        if not hostname:
            show_error(
                "The hostname could not be read. Confirm that your account can run "
                "the appropriate command:\n\nCisco:\n"
                "show running-config | include ^hostname\n\nLinux:\nhostname -s"
            )
            return

        # RemoteAddress is the connected endpoint and is a reliable fallback
        # when a SecureCRT version does not expose the active Hostname option.
        active_config = crt.Session.Config
        address = crt.Session.RemoteAddress
        configured_address = ""
        try:
            configured_address = active_config.GetOption("Hostname")
            if configured_address:
                address = configured_address
        except Exception:
            pass

        if not is_managed_session(current_path, configured_address, crt.Session.RemoteAddress):
            return

        # New ad-hoc connections go to the discovery folder. Once a session is
        # saved or manually moved, hostname changes stay in its current folder.
        target_folder = None if current_path.lower() == "default" else session_parent(current_path)
        session_path = build_session_path(hostname, address, target_folder)
        if current_path.lower() == session_path.lower():
            try:
                crt.GetScriptTab().Caption = hostname
            except Exception:
                pass
            return

        # When Quick Connect's "Save session" option is checked, SecureCRT has
        # already created an IP-named entry. Open that saved configuration so
        # every setting is preserved. For an unsaved Quick Connect session,
        # clone Default and copy the active connection options.
        if current_path.lower() == "default":
            new_config = crt.OpenSessionConfiguration("Default")
            copy_active_options(active_config, new_config)
        else:
            new_config = crt.OpenSessionConfiguration(current_path)

        new_config.SetOption("Hostname", address)
        new_config.Save(session_path)
        queue_cleanup(config_path, current_path, session_path)
        queue_stale_sessions_for_address(config_path, address, session_path)

        # Rename the current tab immediately; the saved entry will be used on
        # subsequent connections.
        try:
            crt.GetScriptTab().Caption = hostname
        except Exception:
            pass

        crt.Session.SetStatusText("Saved session: {}".format(session_path))
        if SHOW_SUCCESS_MESSAGE:
            crt.Dialog.MessageBox(
                "Saved Session Manager entry:\n\n{}\n\nConnection address: {}".format(
                    session_path, address
                ),
                "SecureCRT session saved",
                0x40,
            )
    except Exception as error:
        show_error("The session could not be saved.\n\n{}".format(error))
    finally:
        screen.Synchronous = previous_synchronous


main()
