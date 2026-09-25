# Migration workflow

Version 0.1.0 supports the validation portion of a broader migration process:

1. Preserve the authoritative source model outside this repository.
2. Create the candidate implementation under engineering change control.
3. Export or manually declare reference and candidate topology in a JSON manifest.
4. Choose and document absolute and relative tolerances.
5. Run `opensees-migrationkit validate <manifest>`.
6. Investigate every structured difference; do not hide mismatches by changing expectations or tolerances.
7. When automated checks pass, review the evidence as a qualified engineer.
8. Record human approval separately, with reviewer identity and rationale, only after that review.

Future adapters may automate step 3. Future execution support may add solver-level evidence, but those extensions must preserve the same discrepancy and approval boundaries.
