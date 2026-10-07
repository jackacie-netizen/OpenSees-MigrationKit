import math

import pytest

from opensees_migrationkit.manifest import ToleranceConfig
from opensees_migrationkit.tolerances import numbers_close


def test_exact_values_match():
    assert numbers_close(2.0, 2.0, ToleranceConfig(0.0, 0.0))


def test_absolute_tolerance_boundary_matches():
    assert numbers_close(0.0, 0.1, ToleranceConfig(0.1, 0.0))


def test_relative_tolerance_boundary_matches():
    assert numbers_close(100.0, 101.0, ToleranceConfig(0.0, 1 / 101))


def test_difference_outside_both_tolerances_fails():
    assert not numbers_close(10.0, 10.2, ToleranceConfig(0.01, 0.001))


@pytest.mark.parametrize("value", [math.inf, -math.inf, math.nan])
def test_non_finite_values_are_rejected(value):
    with pytest.raises(ValueError, match="finite"):
        numbers_close(value, 1.0, ToleranceConfig(0.0, 0.0))


def test_negative_runtime_tolerance_is_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        numbers_close(1.0, 1.0, ToleranceConfig(-1.0, 0.0))


def test_programmatic_tolerance_policy_cannot_be_silently_ignored():
    with pytest.raises(ValueError, match="policy"):
        numbers_close(10.0, 11.5, ToleranceConfig(1.0, 0.1, policy="reference_additive"))


@pytest.mark.parametrize(("reference", "candidate"), [(10.0, 11.5), (11.5, 10.0)])
def test_symmetric_max_does_not_apply_additive_reference_tolerance(reference, candidate):
    # Difference 1.5 exceeds both 1.0 absolute and 1.15 relative limits.
    assert not numbers_close(reference, candidate, ToleranceConfig(1.0, 0.1))
