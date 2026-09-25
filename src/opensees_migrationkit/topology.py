"""Structured topology comparison."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .manifest import ToleranceConfig, Topology
from .tolerances import numbers_close


@dataclass(frozen=True)
class Difference:
    category: str
    identifier: int | str
    field: str
    reference: Any
    candidate: Any
    message: str


def _membership_differences(
    category: str,
    reference: dict | object,
    candidate: dict | object,
) -> list[Difference]:
    reference_ids = set(reference)
    candidate_ids = set(candidate)
    differences = [
        Difference(category, identifier, "missing", reference[identifier], None, f"{category} {identifier} is missing from candidate")
        for identifier in sorted(reference_ids - candidate_ids)
    ]
    differences.extend(
        Difference(category, identifier, "extra", None, candidate[identifier], f"{category} {identifier} exists only in candidate")
        for identifier in sorted(candidate_ids - reference_ids)
    )
    return differences


def compare_topologies(
    reference: Topology,
    candidate: Topology,
    tolerance: ToleranceConfig,
) -> tuple[Difference, ...]:
    """Compare node and element topology and return stable structured differences."""

    differences = _membership_differences("node", reference.nodes, candidate.nodes)
    for node_id in sorted(set(reference.nodes) & set(candidate.nodes)):
        expected = reference.nodes[node_id]
        actual = candidate.nodes[node_id]
        if len(expected) != len(actual):
            differences.append(
                Difference("node", node_id, "coordinate_dimension", expected, actual, "node coordinate dimensions differ")
            )
            continue
        for index, (expected_value, actual_value) in enumerate(zip(expected, actual)):
            if not numbers_close(expected_value, actual_value, tolerance):
                differences.append(
                    Difference(
                        "node",
                        node_id,
                        f"coordinate[{index}]",
                        expected_value,
                        actual_value,
                        "node coordinate differs outside tolerance",
                    )
                )

    differences.extend(_membership_differences("element", reference.elements, candidate.elements))
    for element_id in sorted(set(reference.elements) & set(candidate.elements)):
        expected = reference.elements[element_id]
        actual = candidate.elements[element_id]
        if expected != actual:
            differences.append(
                Difference("element", element_id, "connectivity", expected, actual, "element connectivity differs")
            )
    return tuple(differences)
