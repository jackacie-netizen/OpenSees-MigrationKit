# Engineering review

`ENGINEER_REVIEW` means the implemented automated comparisons passed and the evidence is ready for human assessment. It does not mean the migration is approved.

A reviewer should independently examine at least:

- source and target provenance;
- units and coordinate systems;
- declared topology completeness;
- element orientation and connectivity semantics;
- selected tolerance values and their engineering basis;
- limitations of the comparisons performed;
- discrepancies that were resolved outside the tool.

## Separate findings

Review the fidelity of the candidate to the designated baseline separately from the quality of the baseline's physical assumptions. A questionable formulation present in both implementations may be inherited faithfully; changing it creates a model revision that needs its own authorization and baseline identity. A formulation added only by a translation is a different issue. Do not use a desired period, force or stored response as a calibration target.

Record these findings separately:

- the exact input and comparison coverage;
- the automated pass/fail result and all differences;
- the evidence for a discrepancy's cause;
- the engineering recommendation and intended use;
- the human decision, reviewer and rationale.

The existing lifecycle permits `ENGINEER_REVIEW` after automated checks pass. A failed automated check remains `FAILED`. A human may document a scoped disposition outside the automated result, but that note must not rewrite the failed check or suppress its differences. Version 0.1.1 does not implement a residual-waiver or engineering-recommendation engine, and the manual approval API does not accept a `FAILED` record.

## Threshold and residual review

Before validation, identify the source, units, formula and scope of each threshold. Distinguish an executed baseline value, verified solver semantics, a literature-supported method, a project-selected QA cutoff, a reporting filter and an observed regression result. A method reference does not automatically justify a numeric cutoff. If a source or derivation cannot be verified, state that limitation rather than calling it an official requirement.

For a residual, report the measured magnitude, affected component, scale used for relative error and evidence available for its cause. Small magnitude alone does not establish a floating-point explanation. Matching model labels alone does not prove identical definitions. Review whether the difference matters for the specified use, especially near zero or a decision boundary. Missing evidence must remain distinguishable from a passing check.

Decisions about response histories, convergence, modal behavior or equilibrium require evidence beyond this manifest core. The [future adapter requirements](future_adapters.md) describe planned coverage; they do not add current automated checks.

## Human approval evidence

The manual approval API requires a reviewer identifier and an approval note, records that initiation was manual, and accepts only an `ENGINEER_REVIEW` record. The normal `validate` CLI does not expose this API. JSON report schema 1.1 preserves the supplied transition history, including the human event when a human application exports it.

The API records a declaration, not proof of a human identity. An AI agent must not call it to approve real engineering work. Applications using it are responsible for authenticating the reviewer, restricting access, binding the decision to the reviewed input and scope, and retaining the evidence. Directly constructing a record with `APPROVED` is not a verified human approval.
