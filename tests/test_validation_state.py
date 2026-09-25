import pytest

from opensees_migrationkit.validation_state import (
    ValidationRecord,
    ValidationState,
    record_human_approval,
    transition_automated,
)


def test_automated_success_path_reaches_engineer_review():
    record = ValidationRecord()
    record = transition_automated(record, ValidationState.RUNNING)
    record = transition_automated(record, ValidationState.PASSED_AUTOMATED_CHECKS)
    record = transition_automated(record, ValidationState.ENGINEER_REVIEW)
    assert record.state is ValidationState.ENGINEER_REVIEW
    assert all(not event.manual_initiation for event in record.history)


def test_automated_failure_path_reaches_failed():
    record = transition_automated(ValidationRecord(), ValidationState.RUNNING)
    record = transition_automated(record, ValidationState.FAILED)
    assert record.state is ValidationState.FAILED


@pytest.mark.parametrize("start", list(ValidationState))
def test_automated_transition_never_assigns_approved(start):
    with pytest.raises(ValueError, match="human"):
        transition_automated(ValidationRecord(state=start), ValidationState.APPROVED)


def test_invalid_automated_skip_is_rejected():
    with pytest.raises(ValueError, match="Invalid automated transition"):
        transition_automated(ValidationRecord(), ValidationState.ENGINEER_REVIEW)


@pytest.mark.parametrize(("reviewer", "note"), [("", "checked"), ("Engineer", "")])
def test_manual_approval_requires_reviewer_and_note(reviewer, note):
    record = ValidationRecord(state=ValidationState.ENGINEER_REVIEW)
    with pytest.raises(ValueError, match="required"):
        record_human_approval(record, reviewer, note)


def test_manual_approval_records_actor_note_and_manual_flag():
    record = ValidationRecord(state=ValidationState.ENGINEER_REVIEW)
    approved = record_human_approval(record, "Engineer A", "Reviewed model evidence")
    event = approved.history[-1]
    assert approved.state is ValidationState.APPROVED
    assert (event.actor, event.note, event.manual_initiation) == (
        "Engineer A",
        "Reviewed model evidence",
        True,
    )


def test_manual_approval_requires_engineer_review_state():
    with pytest.raises(ValueError, match="ENGINEER_REVIEW"):
        record_human_approval(ValidationRecord(), "Engineer A", "Reviewed")
