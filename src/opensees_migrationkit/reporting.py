"""Deterministic JSON and CSV validation reports."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

from . import __version__
from .comparison import ValidationResult
from .manifest import Manifest
from .topology import Difference
from .validation_state import ValidationRecord


def _json_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return list(value)
    return value


def _difference_data(difference: Difference) -> dict[str, Any]:
    return {
        "category": difference.category,
        "identifier": difference.identifier,
        "field": difference.field,
        "reference": _json_value(difference.reference),
        "candidate": _json_value(difference.candidate),
        "message": difference.message,
    }


def build_report(manifest: Manifest, result: ValidationResult, record: ValidationRecord) -> dict[str, Any]:
    """Build the stable public validation-report object."""

    return {
        "schema_version": "1.1",
        "project": manifest.project,
        "passed": result.passed,
        "validation_state": record.state.value,
        "summary": result.summary,
        "differences": [_difference_data(item) for item in result.differences],
        "provenance": {
            "package_version": __version__,
            "manifest_schema_version": manifest.schema_version,
            "manifest_sha256": manifest.input_sha256,
            "manifest_size_bytes": manifest.input_size_bytes,
            "tcl_source": manifest.tcl_source,
            "python_target": manifest.python_target,
        },
        "units": dict(manifest.units),
        "tolerances": {
            "absolute": manifest.tolerances.absolute,
            "relative": manifest.tolerances.relative,
            "policy": manifest.tolerances.policy,
        },
        "comparison_scope": {
            "checked_fields": ["node_ids", "node_coordinates", "element_ids", "ordered_connectivity", "numerical_values"],
            "solver_execution_performed": False,
            "source_artifacts_verified": False,
        },
        "validation_history": [
            {
                "from_state": event.from_state.value,
                "to_state": event.to_state.value,
                "actor": event.actor,
                "note": event.note,
                "manual_initiation": event.manual_initiation,
            }
            for event in record.history
        ],
    }


def write_json_report(path: str | Path, report: dict[str, Any]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv_report(path: str | Path, differences: Iterable[Difference]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["category", "identifier", "field", "reference", "candidate", "message"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for difference in differences:
            row = _difference_data(difference)
            row["reference"] = json.dumps(row["reference"], sort_keys=True)
            row["candidate"] = json.dumps(row["candidate"], sort_keys=True)
            writer.writerow(row)
