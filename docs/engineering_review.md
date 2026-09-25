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

The manual approval API requires a reviewer identifier and an approval note, records that initiation was manual, and accepts only an `ENGINEER_REVIEW` record. The normal `validate` CLI does not expose this API. Organizational review and record-retention procedures remain the user's responsibility.
