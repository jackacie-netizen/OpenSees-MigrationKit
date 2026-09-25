from opensees_migrationkit.comparison import validate_manifest
from opensees_migrationkit.manifest import load_manifest


def test_matching_manifest_passes(manifest_path):
    result = validate_manifest(load_manifest(manifest_path))
    assert result.passed is True
    assert result.differences == ()
    assert result.summary == {"node_differences": 0, "element_differences": 0, "numerical_differences": 0, "total_differences": 0}


def test_missing_numerical_value_fails(tmp_path, manifest_data):
    import json

    del manifest_data["candidate"]["numerical_values"]["total_mass"]
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    result = validate_manifest(load_manifest(path))
    assert result.passed is False
    assert [(d.identifier, d.field) for d in result.differences] == [("total_mass", "missing")]


def test_numerical_value_outside_tolerance_fails(tmp_path, manifest_data):
    import json

    manifest_data["candidate"]["numerical_values"]["total_mass"] = 10.5
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest_data), encoding="utf-8")
    result = validate_manifest(load_manifest(path))
    assert result.differences[0].field == "value"
    assert result.summary["numerical_differences"] == 1
