"""Strict JSON manifest parsing for declared model data."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping


class ManifestError(ValueError):
    """Raised when a validation manifest does not satisfy the public schema."""


@dataclass(frozen=True)
class ToleranceConfig:
    absolute: float
    relative: float


@dataclass(frozen=True)
class Topology:
    nodes: Mapping[int, tuple[float, ...]]
    elements: Mapping[int, tuple[int, ...]]
    numerical_values: Mapping[str, float]


@dataclass(frozen=True)
class Manifest:
    schema_version: str
    project: str
    tcl_source: str
    python_target: str
    units: Mapping[str, str]
    tolerances: ToleranceConfig
    reference: Topology
    candidate: Topology
    validation_state: str


_REQUIRED_FIELDS = (
    "schema_version",
    "project",
    "tcl_source",
    "python_target",
    "units",
    "tolerances",
    "reference",
    "candidate",
    "validation_state",
)
_VALID_STATES = {
    "NOT_RUN",
    "RUNNING",
    "FAILED",
    "PASSED_AUTOMATED_CHECKS",
    "ENGINEER_REVIEW",
    "APPROVED",
}


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ManifestError(f"{field} must be a JSON object")
    return value


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{field} must be a non-empty string")
    return value


def _finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ManifestError(f"{field} must be a finite number")
    number = float(value)
    if not math.isfinite(number):
        raise ManifestError(f"{field} must be finite")
    return number


def _identifier(raw: Any, field: str) -> int:
    if not isinstance(raw, str):
        raise ManifestError(f"{field} must be a stringified integer ID")
    try:
        identifier = int(raw)
    except ValueError as error:
        raise ManifestError(f"{field} must be a stringified integer ID") from error
    if str(identifier) != raw:
        raise ManifestError(f"{field} must use canonical integer text")
    return identifier


def _parse_tolerances(value: Any) -> ToleranceConfig:
    data = _mapping(value, "tolerances")
    for field in ("absolute", "relative"):
        if field not in data:
            raise ManifestError(f"tolerances.{field} is required")
    absolute = _finite_number(data["absolute"], "tolerances.absolute")
    relative = _finite_number(data["relative"], "tolerances.relative")
    if absolute < 0.0 or relative < 0.0:
        raise ManifestError("tolerances must be non-negative")
    return ToleranceConfig(absolute=absolute, relative=relative)


def _parse_topology(value: Any, field: str) -> Topology:
    data = _mapping(value, field)
    nodes_raw = _mapping(data.get("nodes"), f"{field}.nodes")
    elements_raw = _mapping(data.get("elements"), f"{field}.elements")
    numbers_raw = _mapping(data.get("numerical_values", {}), f"{field}.numerical_values")

    nodes: dict[int, tuple[float, ...]] = {}
    for raw_id, raw_coordinates in nodes_raw.items():
        node_id = _identifier(raw_id, f"{field} node ID")
        if not isinstance(raw_coordinates, list) or not raw_coordinates:
            raise ManifestError(f"{field} node {node_id} coordinates must be a non-empty array")
        nodes[node_id] = tuple(
            _finite_number(value, f"{field} node {node_id} coordinate")
            for value in raw_coordinates
        )

    elements: dict[int, tuple[int, ...]] = {}
    for raw_id, raw_element in elements_raw.items():
        element_id = _identifier(raw_id, f"{field} element ID")
        element_data = _mapping(raw_element, f"{field} element {element_id}")
        connectivity = element_data.get("connectivity")
        if not isinstance(connectivity, list) or not connectivity:
            raise ManifestError(f"{field} element {element_id} connectivity must be a non-empty array")
        if any(isinstance(node, bool) or not isinstance(node, int) for node in connectivity):
            raise ManifestError(f"{field} element {element_id} connectivity must contain integer node IDs")
        elements[element_id] = tuple(connectivity)

    numerical_values: dict[str, float] = {}
    for name, raw_number in numbers_raw.items():
        key = _nonempty_string(name, f"{field} numerical value name")
        numerical_values[key] = _finite_number(raw_number, f"{field}.numerical_values.{key}")

    return Topology(
        nodes=MappingProxyType(nodes),
        elements=MappingProxyType(elements),
        numerical_values=MappingProxyType(numerical_values),
    )


def load_manifest(path: str | Path) -> Manifest:
    """Load and strictly validate a JSON comparison manifest."""

    manifest_path = Path(path)
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ManifestError(f"invalid JSON: {error.msg}") from error
    data = _mapping(raw, "manifest")
    for field in _REQUIRED_FIELDS:
        if field not in data:
            raise ManifestError(f"{field} is required")

    units_data = _mapping(data["units"], "units")
    units = {
        _nonempty_string(key, "unit name"): _nonempty_string(value, f"unit {key}")
        for key, value in units_data.items()
    }
    state = _nonempty_string(data["validation_state"], "validation_state")
    if state not in _VALID_STATES:
        raise ManifestError(f"validation_state is not recognized: {state}")

    return Manifest(
        schema_version=_nonempty_string(data["schema_version"], "schema_version"),
        project=_nonempty_string(data["project"], "project"),
        tcl_source=_nonempty_string(data["tcl_source"], "tcl_source"),
        python_target=_nonempty_string(data["python_target"], "python_target"),
        units=MappingProxyType(units),
        tolerances=_parse_tolerances(data["tolerances"]),
        reference=_parse_topology(data["reference"], "reference"),
        candidate=_parse_topology(data["candidate"], "candidate"),
        validation_state=state,
    )
