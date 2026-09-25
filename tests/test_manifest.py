from __future__ import annotations

import json
import math

import pytest

from opensees_migrationkit.manifest import ManifestError, load_manifest


def test_loads_complete_manifest(manifest_path):
    manifest = load_manifest(manifest_path)
    assert manifest.project == "synthetic-test"
    assert manifest.reference.nodes[3] == (0.0, 3.0)
    assert manifest.reference.elements[1] == (1, 3)
    assert manifest.tolerances.absolute == 1e-9


@pytest.mark.parametrize("field", ["project", "reference", "tolerances"])
def test_rejects_missing_required_field(tmp_path, manifest_data, field):
    del manifest_data[field]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match=field):
        load_manifest(path)


def test_rejects_non_integer_node_key(tmp_path, manifest_data):
    manifest_data["reference"]["nodes"] = {"node-one": [0.0, 0.0]}
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="node ID"):
        load_manifest(path)


def test_rejects_boolean_connectivity_value(tmp_path, manifest_data):
    manifest_data["reference"]["elements"]["1"]["connectivity"] = [True, 3]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="connectivity"):
        load_manifest(path)


@pytest.mark.parametrize(
    ("section", "replacement", "message"),
    [
        ("nodes", {"1": []}, "coordinates"),
        ("elements", {"1": {"connectivity": []}}, "connectivity"),
    ],
)
def test_rejects_empty_topology_values(tmp_path, manifest_data, section, replacement, message):
    manifest_data["reference"][section] = replacement
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match=message):
        load_manifest(path)


def test_rejects_non_finite_coordinate(tmp_path, manifest_data):
    manifest_data["reference"]["nodes"]["1"] = [math.inf, 0.0]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="finite"):
        load_manifest(path)


@pytest.mark.parametrize("field", ["absolute", "relative"])
def test_rejects_negative_tolerance(tmp_path, manifest_data, field):
    manifest_data["tolerances"][field] = -1.0
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    with pytest.raises(ManifestError, match="non-negative"):
        load_manifest(path)
