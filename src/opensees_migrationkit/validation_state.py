"""Validation lifecycle with an explicit human approval boundary."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class ValidationState(str, Enum):
    NOT_RUN = "NOT_RUN"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    PASSED_AUTOMATED_CHECKS = "PASSED_AUTOMATED_CHECKS"
    ENGINEER_REVIEW = "ENGINEER_REVIEW"
    APPROVED = "APPROVED"


@dataclass(frozen=True)
class TransitionEvent:
    from_state: ValidationState
    to_state: ValidationState
    actor: str
    note: str
    manual_initiation: bool


@dataclass(frozen=True)
class ValidationRecord:
    state: ValidationState = ValidationState.NOT_RUN
    history: tuple[TransitionEvent, ...] = ()


_AUTOMATED_TRANSITIONS = {
    ValidationState.NOT_RUN: {ValidationState.RUNNING},
    ValidationState.RUNNING: {ValidationState.FAILED, ValidationState.PASSED_AUTOMATED_CHECKS},
    ValidationState.PASSED_AUTOMATED_CHECKS: {ValidationState.ENGINEER_REVIEW},
}


def transition_automated(record: ValidationRecord, target: ValidationState) -> ValidationRecord:
    """Apply a permitted automated transition; never assign APPROVED."""

    if target is ValidationState.APPROVED:
        raise ValueError("APPROVED requires explicit human approval")
    if target not in _AUTOMATED_TRANSITIONS.get(record.state, set()):
        raise ValueError(f"Invalid automated transition: {record.state.value} -> {target.value}")
    event = TransitionEvent(record.state, target, "automated-validation", "", False)
    return replace(record, state=target, history=record.history + (event,))


def record_human_approval(record: ValidationRecord, reviewer: str, note: str) -> ValidationRecord:
    """Record a manually initiated approval after engineer review."""

    if record.state is not ValidationState.ENGINEER_REVIEW:
        raise ValueError("Human approval requires ENGINEER_REVIEW state")
    if not reviewer.strip() or not note.strip():
        raise ValueError("Reviewer identifier and approval note are required")
    event = TransitionEvent(record.state, ValidationState.APPROVED, reviewer.strip(), note.strip(), True)
    return replace(record, state=ValidationState.APPROVED, history=record.history + (event,))
