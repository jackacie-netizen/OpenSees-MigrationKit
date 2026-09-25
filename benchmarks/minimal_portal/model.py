"""Synthetic portal-frame reference artifact; not executed by the v0.1.0 core."""


def build_model(ops):
    """Build a one-bay, one-storey elastic 2D portal with an OpenSeesPy-like API."""

    ops.model("basic", "-ndm", 2, "-ndf", 3)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 4.0, 0.0)
    ops.node(3, 0.0, 3.0)
    ops.node(4, 4.0, 3.0)
    ops.fix(1, 1, 1, 1)
    ops.fix(2, 1, 1, 1)
    ops.geomTransf("Linear", 1)
    area, elastic_modulus, inertia = 0.02, 2.0e11, 8.0e-5
    ops.element("elasticBeamColumn", 1, 1, 3, area, elastic_modulus, inertia, 1)
    ops.element("elasticBeamColumn", 2, 2, 4, area, elastic_modulus, inertia, 1)
    ops.element("elasticBeamColumn", 3, 3, 4, area, elastic_modulus, inertia, 1)
