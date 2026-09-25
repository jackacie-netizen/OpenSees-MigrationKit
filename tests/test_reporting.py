import csv
import json

from opensees_migrationkit.comparison import validate_manifest
from opensees_migrationkit.manifest import load_manifest
from opensees_migrationkit.reporting import build_report, write_csv_report, write_json_report
from opensees_migrationkit.validation_state import ValidationRecord, ValidationState


def test_build_report_has_stable_public_shape(manifest_path):
    manifest = load_manifest(manifest_path)
    result = validate_manifest(manifest)
    record = ValidationRecord(state=ValidationState.ENGINEER_REVIEW)
    report = build_report(manifest, result, record)
    assert list(report) == ["schema_version", "project", "passed", "validation_state", "summary", "differences"]
    assert report["validation_state"] == "ENGINEER_REVIEW"


def test_json_report_is_sorted_and_newline_terminated(tmp_path, manifest_path):
    manifest = load_manifest(manifest_path)
    report = build_report(manifest, validate_manifest(manifest), ValidationRecord())
    path = tmp_path / "nested" / "report.json"
    write_json_report(path, report)
    text = path.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert json.loads(text)["project"] == "synthetic-test"
    assert text.index('"differences"') < text.index('"passed"')


def test_csv_report_writes_header_and_deterministic_rows(tmp_path, manifest_data):
    from opensees_migrationkit.manifest import ToleranceConfig, Topology
    from opensees_migrationkit.topology import compare_topologies

    reference = Topology(nodes={1: (0.0, 0.0)}, elements={}, numerical_values={})
    candidate = Topology(nodes={2: (1.0, 0.0)}, elements={}, numerical_values={})
    differences = compare_topologies(reference, candidate, ToleranceConfig(0.0, 0.0))
    path = tmp_path / "nested" / "differences.csv"
    write_csv_report(path, differences)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["identifier"] for row in rows] == ["1", "2"]
    assert list(rows[0]) == ["category", "identifier", "field", "reference", "candidate", "message"]
