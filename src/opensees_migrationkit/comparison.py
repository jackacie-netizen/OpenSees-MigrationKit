"""High-level manifest validation."""

from __future__ import annotations

from dataclasses import dataclass

from .manifest import Manifest
from .tolerances import numbers_close
from .topology import Difference, compare_topologies


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    differences: tuple[Difference, ...]
    summary: dict[str, int]


def _compare_numerical_values(manifest: Manifest) -> list[Difference]:
    reference = manifest.reference.numerical_values
    candidate = manifest.candidate.numerical_values
    differences = [
        Difference("numerical", name, "missing", reference[name], None, f"numerical value {name} is missing from candidate")
        for name in sorted(set(reference) - set(candidate))
    ]
    differences.extend(
        Difference("numerical", name, "extra", None, candidate[name], f"numerical value {name} exists only in candidate")
        for name in sorted(set(candidate) - set(reference))
    )
    for name in sorted(set(reference) & set(candidate)):
        if not numbers_close(reference[name], candidate[name], manifest.tolerances):
            differences.append(
                Difference(
                    "numerical",
                    name,
                    "value",
                    reference[name],
                    candidate[name],
                    "numerical value differs outside tolerance",
                )
            )
    return differences


def validate_manifest(manifest: Manifest) -> ValidationResult:
    """Validate candidate data against declared reference data."""

    differences = list(compare_topologies(manifest.reference, manifest.candidate, manifest.tolerances))
    differences.extend(_compare_numerical_values(manifest))
    summary = {
        "node_differences": sum(item.category == "node" for item in differences),
        "element_differences": sum(item.category == "element" for item in differences),
        "numerical_differences": sum(item.category == "numerical" for item in differences),
        "total_differences": len(differences),
    }
    return ValidationResult(passed=not differences, differences=tuple(differences), summary=summary)
