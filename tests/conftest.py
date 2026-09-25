from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def manifest_data() -> dict:
    topology = {
        "nodes": {"1": [0.0, 0.0], "2": [4.0, 0.0], "3": [0.0, 3.0]},
        "elements": {
            "1": {"connectivity": [1, 3]},
            "2": {"connectivity": [3, 2]},
        },
        "numerical_values": {"total_mass": 10.0},
    }
    return {
        "schema_version": "1.0",
        "project": "synthetic-test",
        "tcl_source": "model.tcl",
        "python_target": "model.py",
        "units": {"length": "m", "force": "N"},
        "tolerances": {"absolute": 1e-9, "relative": 1e-6},
        "reference": json.loads(json.dumps(topology)),
        "candidate": json.loads(json.dumps(topology)),
        "validation_state": "NOT_RUN",
    }


@pytest.fixture
def manifest_path(tmp_path: Path, manifest_data: dict) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    return path
