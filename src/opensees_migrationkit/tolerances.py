"""Explicit numerical tolerance comparisons."""

from __future__ import annotations

import math

from .manifest import ToleranceConfig


def numbers_close(reference: float, candidate: float, tolerance: ToleranceConfig) -> bool:
    """Apply symmetric_max: abs(delta) <= max(atol, rtol * max(abs(a), abs(b)))."""

    if tolerance.policy != "symmetric_max":
        raise ValueError("unsupported tolerance policy; expected symmetric_max")
    values = (float(reference), float(candidate), tolerance.absolute, tolerance.relative)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("comparison values and tolerances must be finite")
    if tolerance.absolute < 0.0 or tolerance.relative < 0.0:
        raise ValueError("tolerances must be non-negative")
    difference = abs(values[1] - values[0])
    limit = max(tolerance.absolute, tolerance.relative * max(abs(values[0]), abs(values[1])))
    return difference <= limit
