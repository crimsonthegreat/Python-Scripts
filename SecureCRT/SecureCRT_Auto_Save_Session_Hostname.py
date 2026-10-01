# $language = "Python3"
# $interface = "1.0"

"""
SecureCRT: discover a hostname from the existing prompt and save an IP-based session.

Set this file as the logon script under Connection > Logon Actions.
Supported prompts include Cisco switch#, ISE hostname/user#,
Palo Alto admin@firewall(active)>,
and Linux user@server:~$ or [user@server ~]$.
No commands or keystrokes are sent to the device. Linux prompts must include
the hostname. Discovery waits up to COMMAND_TIMEOUT_SECONDS for a prompt.
Saved sessions retain their current folder when their hostname changes.
Cleanup is optional and restricted to a hostname-named source when its hostname
changes and a new replacement session is created. Old entries are backed up and removed only after connecting
to the replacement. Legacy cleanup queues are never processed.
"""

import re
import os
import json
import hashlib
import shutil
import uuid
import datetime


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

# Temporary diagnosis: turn off after cleanup is confirmed working.
DEBUG_CLEANUP = False
SCRIPT_VERSION = "hostname-cleanup-9"

# Maximum time to wait for a recognizable prompt.
COMMAND_TIMEOUT_SECONDS = 15

# Optional safe cleanup: set this to your SecureCRT configuration directory
# (the directory containing Sessions). Leave blank to retain all old entries.
# Windows example: r"C:\Users\you\AppData\Roaming\VanDyke\Config"
# macOS example: "/Users/you/Library/Application Support/VanDyke/SecureCRT/Config"
SECURECRT_CONFIG_DIRECTORY = ""
SAFE_CLEANUP_QUEUE = "AutoSaveSessionHostnameCleanup-v3.json"
SAFE_CLEANUP_BACKUPS = "AutoSaveSessionSafeBackups"

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


def discover_hostname(screen, prompt):
    """Extract a hostname from a supported prompt without sending input."""
    prompt = clean_terminal_text(prompt).strip()
    # Cisco ISE / ADE-OS: hostname/user#
    match = re.fullmatch(
        r"(?P<hostname>[A-Za-z0-9_.-]+)/[^/\s#]+[ \t]*#",
        prompt,
    )
    if match:
        return sanitize_session_component(match.group("hostname"))

    match = re.fullmatch(
        r"\[?[^@\s]+@"
        r"(?P<hostname>[A-Za-z0-9_.-]+)"
        r"(?:\([^()\r\n]*\))?"
        r"(?::[^\r\n]*|[ \t]+[^\r\n]*)?"
        r"\]?[ \t]*[#$%>]",
        prompt,
    )
    if match:
        return sanitize_session_component(match.group("hostname"))

    match = re.fullmatch(
        r"(?P<hostname>[A-Za-z0-9_.-]+)"
        r"(?:\([^()\r\n]*\))?"
        r"[ \t]*[#>]",
        prompt,
    )
    if match:
        return sanitize_session_component(match.group("hostname"))
    return ""


def get_prompt(screen):
    """Process incoming text and inspect the prompt without sending input."""
    for _ in range(COMMAND_TIMEOUT_SECONDS):
        if not crt.Session.Connected:
            return ""
        screen.WaitForString("__AUTOSAVE_PROMPT_SENTINEL__", 1)
        row = screen.CurrentRow
        column = screen.CurrentColumn
        if column <= 1:
            continue
        prompt = clean_terminal_text(
            screen.Get(row, 1, row, column - 1)
        ).strip()
        if discover_hostname(screen, prompt):
            return prompt
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


def is_managed_session(path, configured_address, remote_address):
    """All saved Session Manager entries and ad-hoc sessions are managed."""
    return bool(path)


def session_parent(path):
    """Return the Session Manager folder containing a saved session."""
    normalized = path.replace("/", "\\")
    parts = normalized.split("\\")
    return "\\".join(parts[:-1])


def normalized_session_path(path):
    """Compare SecureCRT API and saved paths independent of slash format."""
    return path.replace("/", "\\").casefold()


def safe_session_file(session_path):
    """Resolve a session below the explicitly configured Sessions directory."""
    directory = os.path.expandvars(os.path.expanduser(SECURECRT_CONFIG_DIRECTORY))
    root = os.path.realpath(os.path.join(directory, "Sessions"))
    parts = session_path.replace("\\", "/").split("/")
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ValueError("Unsafe session path")
    path = os.path.realpath(os.path.join(root, *parts) + ".ini")
    if os.path.commonpath((root, path)) != root:
        raise ValueError("Session path escaped Sessions directory")
    return path


def file_digest(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def read_safe_queue():
    path = os.path.join(SECURECRT_CONFIG_DIRECTORY, SAFE_CLEANUP_QUEUE)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        entries = json.load(handle)
    if not isinstance(entries, list):
        raise ValueError("Invalid safe cleanup queue")
    return entries


def write_safe_queue(entries):
    path = os.path.join(SECURECRT_CONFIG_DIRECTORY, SAFE_CLEANUP_QUEUE)
    temporary = path + "." + uuid.uuid4().hex + ".tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2)
    os.replace(temporary, path)


def connection_identity(config):
    hostname = str(config.GetOption("Hostname")).strip()
    protocol = str(config.GetOption("Protocol Name")).strip()
    username = str(config.GetOption("Username")).strip()
    # SecureCRT uses protocol-specific option names in some versions.
    for option in ("[{}] Port".format(protocol), "Port"):
        try:
            port = str(config.GetOption(option)).strip()
            if port:
                return hostname, protocol, port, username
        except Exception:
            continue
    raise ValueError("Cannot verify the session port; cleanup disabled for this save")


def saved_session_hostname(path, address):
    """Recognize names generated by this script; exclude IP-named sessions."""
    leaf = re.split(r"[\\/]", path)[-1].strip()
    suffix = " [{}]".format(address)
    if leaf.endswith(suffix):
        leaf = leaf[:-len(suffix)]
    elif INCLUDE_IP_IN_SESSION_NAME:
        return ""
    if leaf == address or path.lower() == "default":
        return ""
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", leaf):
        return ""
    return leaf


def hostname_changed(old_path, new_path, address):
    old_hostname = saved_session_hostname(old_path, address)
    new_hostname = saved_session_hostname(new_path, address)
    return bool(old_hostname and new_hostname
                and old_hostname.casefold() != new_hostname.casefold())


def record_safe_replacement(old_path, new_path, old_digest, identity):
    """Record only a newly created replacement after a hostname change."""
    if not hostname_changed(old_path, new_path, identity[0]):
        return
    old_file = safe_session_file(old_path)
    new_file = safe_session_file(new_path)
    if file_digest(old_file) != old_digest or os.path.getsize(new_file) == 0:
        return
    saved = crt.OpenSessionConfiguration(new_path)
    if connection_identity(saved) != identity:
        return
    entries = read_safe_queue()
    entries = [entry for entry in entries
               if normalized_session_path(entry.get("old_path", ""))
               != normalized_session_path(old_path)]
    entries.append({"old_path": old_path, "new_path": new_path,
                    "old_digest": old_digest, "new_digest": file_digest(new_file),
                    "identity": list(identity)})
    write_safe_queue(entries)


def process_safe_cleanup(current_path, detected_hostname):
    """Delete verified inactive sources after backing up their current contents."""
    if not SECURECRT_CONFIG_DIRECTORY:
        return "Cleanup disabled: SECURECRT_CONFIG_DIRECTORY is blank"
    # Fail closed if SecureCRT cannot enumerate every active tab.
    active_paths = set()
    for index in range(1, crt.GetTabCount() + 1):
        tab = crt.GetTab(index)
        if tab.Session.Connected:
            active_paths.add(normalized_session_path(tab.Session.Path))
    entries = read_safe_queue()
    if not entries:
        return "No pending cleanup entries in the configured queue"
    remaining = []
    notes = []
    for entry in entries:
        try:
            old_path, new_path = entry["old_path"], entry["new_path"]
            if normalized_session_path(new_path) != normalized_session_path(current_path):
                remaining.append(entry)
                continue
            if normalized_session_path(old_path) in active_paths:
                notes.append("Cleanup pending: close/disconnect the old session tab")
                remaining.append(entry)
                continue
            if normalized_session_path(old_path) == normalized_session_path(new_path):
                continue
            old_file, new_file = safe_session_file(old_path), safe_session_file(new_path)
            if not os.path.exists(old_file):
                continue
            identity = tuple(entry["identity"])
            if not hostname_changed(old_path, new_path, identity[0]):
                continue
            if connection_identity(crt.OpenSessionConfiguration(old_path)) != identity:
                notes.append("Cleanup skipped: the old session connection settings have changed")
                remaining.append(entry)
                continue
            # SecureCRT may update session metadata on disconnect. Back up the
            # current source bytes, preserving any other configuration edits.
            current_old_digest = file_digest(old_file)
            if (not os.path.isfile(new_file) or os.path.getsize(new_file) == 0
                    or connection_identity(crt.OpenSessionConfiguration(new_path)) != identity
                    or saved_session_hostname(new_path, identity[0]).casefold()
                    != detected_hostname.casefold()):
                notes.append("Cleanup skipped: replacement identity or hostname could not be verified")
                remaining.append(entry)
                continue
            backup_directory = os.path.join(
                SECURECRT_CONFIG_DIRECTORY, SAFE_CLEANUP_BACKUPS,
                datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex)
            os.makedirs(backup_directory)
            backup = os.path.join(backup_directory, "session.ini")
            shutil.copy2(old_file, backup)
            with open(os.path.join(backup_directory, "restore.json"), "w", encoding="utf-8") as handle:
                json.dump({"original_session_path": old_path}, handle, indent=2)
            if (file_digest(backup) == current_old_digest
                    and file_digest(old_file) == current_old_digest
                    and connection_identity(crt.OpenSessionConfiguration(old_path)) == identity
                    and connection_identity(crt.OpenSessionConfiguration(new_path)) == identity):
                os.remove(old_file)
                notes.append("Old session backed up and deleted: " + old_path)
            else:
                notes.append("Cleanup skipped: a session changed during backup verification")
                remaining.append(entry)
        except Exception as error:
            notes.append("Cleanup skipped: {}".format(error))
            remaining.append(entry)
    write_safe_queue(remaining)
    return " | ".join(notes) or "No queued replacement matches the connected session path"


def main():
    if not crt.Session.Connected:
        show_error("No connected session is active.")
        return

    current_path = crt.Session.Path

    screen = crt.Screen
    previous_synchronous = screen.Synchronous
    screen.Synchronous = True

    try:
        prompt = get_prompt(screen)
        hostname = discover_hostname(screen, prompt)
        if not hostname:
            show_error(
                "The hostname could not be extracted from the prompt.\n\n"
                "Script version: hostname-cleanup-9\n\n"
                "Supported examples:\n"
                "Cisco: switch#\n"
                "Cisco ISE: hostname/user#\n"
                "Palo Alto: admin@firewall(active)>\n"
                "Linux: user@server:~$ or [user@server ~]$\n\n"
                "Linux prompts must include the hostname."
            )
            return

        cleanup_result = ""
        try:
            cleanup_result = process_safe_cleanup(current_path, hostname) or ""
        except Exception as error:
            cleanup_result = "Cleanup skipped: {}".format(error)
        if DEBUG_CLEANUP:
            queue_path = os.path.join(SECURECRT_CONFIG_DIRECTORY, SAFE_CLEANUP_QUEUE)
            crt.Dialog.MessageBox(
                "Version: {}\nConnected session: {}\nDetected hostname: {}\n"
                "Configuration directory: {}\nQueue exists: {}\n\n{}".format(
                    SCRIPT_VERSION, current_path, hostname,
                    SECURECRT_CONFIG_DIRECTORY or "(blank)",
                    os.path.isfile(queue_path), cleanup_result or "No result returned",
                ),
                "AutoSaveSession cleanup diagnostics",
                0x40,
            )
        if cleanup_result:
            crt.Session.SetStatusText(cleanup_result)

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
        if normalized_session_path(current_path) == normalized_session_path(session_path):
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

        cleanup_candidate = None
        cleanup_note = cleanup_result
        if SECURECRT_CONFIG_DIRECTORY:
            try:
                target_file = safe_session_file(session_path)
                # Never overwrite an existing target when safe cleanup is enabled.
                if os.path.exists(target_file):
                    crt.GetScriptTab().Caption = hostname
                    crt.Session.SetStatusText("Existing saved session retained: " + session_path)
                    return
                if (current_path.lower() != "default"
                        and hostname_changed(current_path, session_path, address)):
                    cleanup_candidate = (
                        current_path, session_path,
                        file_digest(safe_session_file(current_path)),
                        connection_identity(active_config),
                    )
            except Exception as error:
                # Cleanup failure must never prevent saving the replacement.
                cleanup_candidate = None
                cleanup_note = "Old session retained: {}".format(error)

        new_config.SetOption("Hostname", address)
        new_config.Save(session_path)
        if cleanup_candidate:
            try:
                record_safe_replacement(*cleanup_candidate)
            except Exception as error:
                cleanup_note = "Old session retained: {}".format(error)

        # Rename the current tab immediately. The original saved session remains
        # available alongside the newly saved entry.
        try:
            crt.GetScriptTab().Caption = hostname
        except Exception:
            pass

        status = "Saved session: {}".format(session_path)
        if cleanup_note:
            status += " | " + cleanup_note
        crt.Session.SetStatusText(status)
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
