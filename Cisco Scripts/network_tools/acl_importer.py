from __future__ import annotations

import csv
import ipaddress
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


VALID_ACTIONS = {"permit", "deny"}
VALID_PROTOCOLS = {"ip", "tcp", "udp", "icmp"}
VALID_PORT_OPERATORS = {"eq", "neq", "lt", "gt", "range"}


@dataclass(frozen=True)
class ACLRule:
    acl_name: str
    acl_type: str
    action: str = ""
    source: str = "any"
    protocol: str = "ip"
    destination: str = "any"
    sequence: int | None = None
    source_port_operator: str | None = None
    source_port: str | None = None
    destination_port_operator: str | None = None
    destination_port: str | None = None
    log: bool = False
    remark: str | None = None

    def to_ios(self) -> str:
        prefix = f"{self.sequence} " if self.sequence is not None else ""
        if self.remark:
            return f"{prefix}remark {self.remark}"

        parts = [prefix + self.action]
        if self.acl_type == "standard":
            parts.append(normalize_address(self.source))
        else:
            parts.extend([self.protocol, normalize_address(self.source)])
            _append_port(parts, self.source_port_operator, self.source_port)
            parts.append(normalize_address(self.destination))
            _append_port(parts, self.destination_port_operator, self.destination_port)
        if self.log:
            parts.append("log")
        return " ".join(parts)


def load_acl_rules(file_path: str | Path) -> list[ACLRule]:
    """Load and validate ACL rules from a .yaml/.yml or .csv file."""
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        rows = _read_yaml(path)
    elif suffix == ".csv":
        rows = _read_csv(path)
    else:
        raise ValueError("ACL rule file must be CSV, YAML, or YML.")

    rules = [_rule_from_mapping(row, index) for index, row in enumerate(rows, 1)]
    _validate_rule_set(rules)
    return rules


def build_acl_command_sets(rules: Iterable[ACLRule]) -> dict[tuple[str, str], list[str]]:
    """Group normalized rules into IOS named-ACL configuration command sets."""
    grouped: dict[tuple[str, str], list[ACLRule]] = defaultdict(list)
    for rule in rules:
        grouped[(rule.acl_type, rule.acl_name)].append(rule)

    commands: dict[tuple[str, str], list[str]] = {}
    for key, acl_rules in grouped.items():
        ordered = sorted(
            enumerate(acl_rules),
            key=lambda item: (
                item[1].sequence is None,
                item[1].sequence if item[1].sequence is not None else item[0],
            ),
        )
        acl_type, acl_name = key
        commands[key] = [
            f"ip access-list {acl_type} {acl_name}",
            *(rule.to_ios() for _, rule in ordered),
        ]
    return commands


def apply_acl_rules(connection: Any, rules: Iterable[ACLRule], *, save: bool = True,
                    dry_run: bool = False) -> dict[str, Any]:
    """Apply imported rules through an established Netmiko connection."""
    command_sets = build_acl_command_sets(rules)
    planned = [command for commands in command_sets.values() for command in commands]
    if dry_run:
        return {"changed": False, "commands": planned, "output": []}

    outputs: list[str] = []
    for (acl_type, acl_name), commands in command_sets.items():
        _ensure_compatible_existing_acl(connection, acl_name, acl_type)
        outputs.append(connection.send_config_set(commands))

    if save and command_sets:
        outputs.append(connection.save_config())
    return {"changed": bool(command_sets), "commands": planned, "output": outputs}


def normalize_address(value: str) -> str:
    value = str(value).strip()
    if value.lower() == "any":
        return "any"
    if value.lower().startswith("host "):
        return f"host {ipaddress.IPv4Address(value.split(maxsplit=1)[1])}"
    if " " in value:
        network, wildcard = value.split()
        ipaddress.IPv4Address(network)
        ipaddress.IPv4Address(wildcard)
        return f"{network} {wildcard}"

    parsed = ipaddress.ip_network(value, strict=False)
    if parsed.version != 4:
        raise ValueError(f"Only IPv4 ACL addresses are supported: {value}")
    if parsed.prefixlen == 32:
        return f"host {parsed.network_address}"
    return f"{parsed.network_address} {parsed.hostmask}"


def _read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _read_yaml(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        document = yaml.safe_load(handle) or {}
    if not isinstance(document, dict) or not isinstance(document.get("acls"), list):
        raise ValueError("YAML file must contain an 'acls' list.")

    rows: list[dict[str, Any]] = []
    for acl in document["acls"]:
        if not isinstance(acl, dict) or not isinstance(acl.get("rules"), list):
            raise ValueError("Each YAML ACL must contain a 'rules' list.")
        for rule in acl["rules"]:
            if not isinstance(rule, dict):
                raise ValueError("Each YAML ACL rule must be a mapping.")
            rows.append({"acl_name": acl.get("name"), "acl_type": acl.get("type"), **rule})
    return rows


def _rule_from_mapping(row: dict[str, Any], row_number: int) -> ACLRule:
    def text_value(name: str, default: str | None = None) -> str | None:
        value = row.get(name, default)
        return default if value is None or str(value).strip() == "" else str(value).strip()

    try:
        sequence_text = text_value("sequence")
        sequence = int(sequence_text) if sequence_text is not None else None
        rule = ACLRule(
            acl_name=text_value("acl_name") or "",
            acl_type=(text_value("acl_type") or "").lower(),
            action=(text_value("action") or "").lower(),
            source=text_value("source", "any") or "any",
            protocol=(text_value("protocol", "ip") or "ip").lower(),
            destination=text_value("destination", "any") or "any",
            sequence=sequence,
            source_port_operator=_lower_or_none(text_value("source_port_operator")),
            source_port=text_value("source_port"),
            destination_port_operator=_lower_or_none(text_value("destination_port_operator")),
            destination_port=text_value("destination_port"),
            log=_as_bool(row.get("log", False)),
            remark=text_value("remark"),
        )
        _validate_rule(rule)
        return rule
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid ACL rule at imported row {row_number}: {exc}") from exc


def _validate_rule(rule: ACLRule) -> None:
    if not rule.acl_name:
        raise ValueError("acl_name/name is required")
    if rule.acl_type not in {"standard", "extended"}:
        raise ValueError("acl_type/type must be standard or extended")
    if rule.sequence is not None and rule.sequence < 1:
        raise ValueError("sequence must be positive")
    if rule.remark:
        return
    if rule.action not in VALID_ACTIONS:
        raise ValueError("action must be permit or deny")
    normalize_address(rule.source)
    if rule.acl_type == "standard":
        if any((rule.source_port_operator, rule.source_port,
                rule.destination_port_operator, rule.destination_port)):
            raise ValueError("standard ACL rules cannot contain port fields")
        return
    if rule.protocol not in VALID_PROTOCOLS:
        raise ValueError(f"protocol must be one of: {', '.join(sorted(VALID_PROTOCOLS))}")
    normalize_address(rule.destination)
    for operator, ports in (
        (rule.source_port_operator, rule.source_port),
        (rule.destination_port_operator, rule.destination_port),
    ):
        _validate_port_expression(operator, ports, rule.protocol)


def _validate_rule_set(rules: list[ACLRule]) -> None:
    acl_types: dict[str, str] = {}
    sequences: dict[tuple[str, str], set[int]] = defaultdict(set)
    for rule in rules:
        previous_type = acl_types.setdefault(rule.acl_name, rule.acl_type)
        if previous_type != rule.acl_type:
            raise ValueError(f"ACL {rule.acl_name!r} has conflicting types.")
        if rule.sequence is not None:
            key = (rule.acl_type, rule.acl_name)
            if rule.sequence in sequences[key]:
                raise ValueError(f"Duplicate sequence {rule.sequence} in ACL {rule.acl_name!r}.")
            sequences[key].add(rule.sequence)


def _validate_port_expression(operator: str | None, ports: str | None, protocol: str) -> None:
    if operator is None and ports is None:
        return
    if protocol not in {"tcp", "udp"}:
        raise ValueError("port fields are valid only with tcp or udp")
    if operator not in VALID_PORT_OPERATORS or not ports:
        raise ValueError("a valid port operator and port value are both required")
    values = str(ports).replace(",", " ").split()
    expected = 2 if operator == "range" else 1
    if len(values) != expected:
        raise ValueError(f"operator {operator} requires {expected} port value(s)")
    for value in values:
        if not value.isdigit() or not 1 <= int(value) <= 65535:
            raise ValueError(f"port must be between 1 and 65535: {value}")


def _append_port(parts: list[str], operator: str | None, ports: str | None) -> None:
    if operator and ports:
        parts.extend([operator, *str(ports).replace(",", " ").split()])


def _ensure_compatible_existing_acl(connection: Any, acl_name: str, acl_type: str) -> None:
    output = connection.send_command(f"show ip access-list {acl_name}").lower()
    if "standard ip access list" in output and acl_type != "standard":
        raise ValueError(f"Existing ACL {acl_name!r} is standard, not {acl_type}.")
    if "extended ip access list" in output and acl_type != "extended":
        raise ValueError(f"Existing ACL {acl_name!r} is extended, not {acl_type}.")


def _lower_or_none(value: str | None) -> str | None:
    return value.lower() if value else None


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "yes", "1", "on"}:
        return True
    if normalized in {"false", "no", "0", "off", ""}:
        return False
    raise ValueError(f"invalid boolean value: {value}")
