from __future__ import annotations

import json
from pathlib import Path

from opensees_migrationkit.cli import build_parser, main


def test_cli_help_exposes_validate_only(capsys):
    parser = build_parser()
    help_text = parser.format_help()
    assert "validate" in help_text
    assert "approve" not in help_text


def test_validate_passes_and_reaches_engineer_review(manifest_path, capsys):
    assert main(["validate", str(manifest_path)]) == 0
    assert "PASS state=ENGINEER_REVIEW differences=0" in capsys.readouterr().out


def test_validate_failure_returns_one(tmp_path, manifest_data, capsys):
    manifest_data["candidate"]["nodes"]["1"] = [0.5, 0.0]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    assert main(["validate", str(path)]) == 1
    assert "FAIL state=FAILED" in capsys.readouterr().out


def test_validate_writes_requested_reports(tmp_path, manifest_path):
    json_path = tmp_path / "report.json"
    csv_path = tmp_path / "report.csv"
    assert main(["validate", str(manifest_path), "--json-report", str(json_path), "--csv-report", str(csv_path)]) == 0
    assert json.loads(json_path.read_text(encoding="utf-8"))["passed"] is True
    assert csv_path.read_text(encoding="utf-8").startswith("category,identifier,field")


def test_invalid_json_returns_one(tmp_path, capsys):
    path = tmp_path / "invalid.json"
    path.write_text("{", encoding="utf-8")
    assert main(["validate", str(path)]) == 1
    assert "Invalid manifest" in capsys.readouterr().err


def test_checked_in_minimal_portal_manifest_validates(capsys):
    manifest = Path(__file__).parents[1] / "benchmarks" / "minimal_portal" / "manifest.json"
    assert main(["validate", str(manifest)]) == 0
    assert "PASS state=ENGINEER_REVIEW" in capsys.readouterr().out
