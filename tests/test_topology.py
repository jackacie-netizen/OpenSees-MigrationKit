from opensees_migrationkit.manifest import ToleranceConfig, Topology
from opensees_migrationkit.topology import compare_topologies


TOL = ToleranceConfig(absolute=1e-6, relative=1e-6)


def topology(nodes=None, elements=None):
    return Topology(nodes=nodes or {}, elements=elements or {}, numerical_values={})


def test_matching_topology_has_no_differences():
    model = topology({1: (0.0, 0.0)}, {1: (1, 2)})
    assert compare_topologies(model, model, TOL) == ()


def test_reports_missing_and_extra_nodes():
    reference = topology({1: (0.0, 0.0), 2: (1.0, 0.0)})
    candidate = topology({2: (1.0, 0.0), 3: (2.0, 0.0)})
    differences = compare_topologies(reference, candidate, TOL)
    assert [(d.identifier, d.field) for d in differences] == [(1, "missing"), (3, "extra")]


def test_reports_coordinate_mismatch():
    reference = topology({1: (0.0, 0.0)})
    candidate = topology({1: (0.0, 0.01)})
    difference = compare_topologies(reference, candidate, TOL)[0]
    assert (difference.category, difference.identifier, difference.field) == ("node", 1, "coordinate[1]")


def test_reports_coordinate_dimension_mismatch():
    reference = topology({1: (0.0, 0.0)})
    candidate = topology({1: (0.0, 0.0, 0.0)})
    difference = compare_topologies(reference, candidate, TOL)[0]
    assert difference.field == "coordinate_dimension"


def test_reports_missing_extra_and_connectivity_mismatch():
    reference = topology(elements={1: (1, 2), 2: (2, 3)})
    candidate = topology(elements={1: (2, 1), 3: (3, 4)})
    differences = compare_topologies(reference, candidate, TOL)
    assert [(d.identifier, d.field) for d in differences] == [
        (2, "missing"),
        (3, "extra"),
        (1, "connectivity"),
    ]
