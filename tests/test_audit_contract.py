"""Regression tests for input integrity and portable audit evidence."""

import hashlib
import json

import pytest

from opensees_migrationkit.cli import main
from opensees_migrationkit.comparison import validate_manifest
from opensees_migrationkit.manifest import ManifestError, load_manifest
from opensees_migrationkit.reporting import build_report
from opensees_migrationkit.validation_state import (
    ValidationRecord,
    ValidationState,
    record_human_approval,
    transition_automated,
)


@pytest.mark.parametrize("version", ["0.0", "1.1", "999.0"])
def test_unsupported_manifest_schema_is_rejected(tmp_path, manifest_data, version):
    manifest_data["schema_version"] = version
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="schema_version"):
        load_manifest(path)


@pytest.mark.parametrize(
    ("original", "duplicate"),
    [
        ('"project": "synthetic-test"', '"project": "discarded", "project": "synthetic-test"'),
        ('"1": [0.0, 0.0]', '"1": [9.0, 9.0], "1": [0.0, 0.0]'),
        ('"absolute": 1e-09', '"absolute": 1.0, "absolute": 1e-09'),
    ],
)
def test_duplicate_json_keys_cannot_hide_data(tmp_path, manifest_data, original, duplicate):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data).replace(original, duplicate, 1), encoding="utf-8")
    with pytest.raises(ManifestError, match="duplicate"):
        load_manifest(path)


@pytest.mark.parametrize("location", ["manifest", "tolerances", "reference", "element"])
def test_unknown_fields_are_not_silently_ignored(tmp_path, manifest_data, location):
    target = {
        "manifest": manifest_data,
        "tolerances": manifest_data["tolerances"],
        "reference": manifest_data["reference"],
        "element": manifest_data["candidate"]["elements"]["1"],
    }[location]
    target["unverified_field"] = "synthetic-extra-data"
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="unverified_field"):
        load_manifest(path)


@pytest.mark.parametrize("side", ["reference", "candidate"])
def test_connectivity_requires_declared_nodes(tmp_path, manifest_data, side):
    manifest_data[side]["elements"]["1"]["connectivity"] = [1, 999]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="999"):
        load_manifest(path)


def test_unknown_tolerance_policy_is_rejected(tmp_path, manifest_data):
    manifest_data["tolerances"]["policy"] = "reference_additive"
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="policy"):
        load_manifest(path)


def test_explicit_supported_policy_is_preserved(tmp_path, manifest_data):
    manifest_data["tolerances"]["policy"] = "symmetric_max"
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    manifest = load_manifest(path)
    assert manifest.tolerances.policy == "symmetric_max"


def test_report_preserves_input_identity_units_and_tolerances(manifest_path):
    original_bytes = manifest_path.read_bytes()
    manifest = load_manifest(manifest_path)
    # The report must identify the bytes actually loaded, not a later file revision.
    manifest_path.write_text("{}", encoding="utf-8")
    report = build_report(manifest, validate_manifest(manifest), ValidationRecord())
    assert report["provenance"]["manifest_sha256"] == hashlib.sha256(original_bytes).hexdigest()
    assert report["provenance"]["manifest_size_bytes"] == len(original_bytes)
    assert report["provenance"]["manifest_schema_version"] == "1.0"
    assert report["provenance"]["tcl_source"] == "model.tcl"
    assert report["provenance"]["python_target"] == "model.py"
    assert report["units"] == {"length": "m", "force": "N"}
    assert report["tolerances"] == {"absolute": 1e-9, "relative": 1e-6, "policy": "symmetric_max"}
    assert report["comparison_scope"]["solver_execution_performed"] is False
    assert report["comparison_scope"]["source_artifacts_verified"] is False


def test_json_report_retains_manual_approval_audit_event(manifest_path):
    manifest = load_manifest(manifest_path)
    record = ValidationRecord()
    for state in (ValidationState.RUNNING, ValidationState.PASSED_AUTOMATED_CHECKS, ValidationState.ENGINEER_REVIEW):
        record = transition_automated(record, state)
    record = record_human_approval(record, "Synthetic reviewer", "Synthetic test review only")
    report = build_report(manifest, validate_manifest(manifest), record)
    assert len(report["validation_history"]) == 4
    assert report["validation_history"][-1] == {
        "from_state": "ENGINEER_REVIEW",
        "to_state": "APPROVED",
        "actor": "Synthetic reviewer",
        "note": "Synthetic test review only",
        "manual_initiation": True,
    }
    assert all(not event["manual_initiation"] for event in report["validation_history"][:-1])


def test_invalid_connectivity_cli_fails_without_success_report(tmp_path, manifest_data, capsys):
    manifest_data["candidate"]["elements"]["1"]["connectivity"] = [1, 999]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    output = tmp_path / "report.json"
    assert main(["validate", str(path), "--json-report", str(output)]) == 1
    assert "999" in capsys.readouterr().err
    assert not output.exists()


def test_failed_comparison_retains_failed_state_and_evidence(tmp_path, manifest_data):
    manifest_data["candidate"]["nodes"]["1"] = [0.5, 0.0]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    output = tmp_path / "report.json"
    assert main(["validate", str(path), "--json-report", str(output)]) == 1
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["passed"] is False
    assert report["validation_state"] == "FAILED"
    assert report["validation_history"][-1]["to_state"] == "FAILED"
    assert len(report["differences"]) == 1


def test_cli_success_has_automated_history_but_no_approval(tmp_path, manifest_path):
    output = tmp_path / "report.json"
    assert main(["validate", str(manifest_path), "--json-report", str(output)]) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert [event["to_state"] for event in report["validation_history"]] == [
        "RUNNING", "PASSED_AUTOMATED_CHECKS", "ENGINEER_REVIEW",
    ]
    assert all(not event["manual_initiation"] for event in report["validation_history"])


def test_invalid_utf8_is_a_manifest_error(tmp_path, capsys):
    path = tmp_path / "manifest.json"
    path.write_bytes(b"\xff\xfe")
    assert main(["validate", str(path)]) == 1
    assert "UTF-8" in capsys.readouterr().err


def test_report_identity_includes_json_whitespace(tmp_path, manifest_data):
    compact = tmp_path / "compact.json"
    formatted = tmp_path / "formatted.json"
    compact.write_text(json.dumps(manifest_data), encoding="utf-8")
    formatted.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    first = load_manifest(compact)
    second = load_manifest(formatted)
    assert validate_manifest(first).passed and validate_manifest(second).passed
    assert first.input_sha256 != second.input_sha256
    assert first.input_sha256 == hashlib.sha256(compact.read_bytes()).hexdigest()
    assert second.input_sha256 == hashlib.sha256(formatted.read_bytes()).hexdigest()
