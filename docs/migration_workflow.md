# Migration workflow

Version 0.1.1 supports the validation portion of a broader migration process:

1. Preserve the authoritative source model outside this repository and record the selected baseline identity, version and authorized scope.
2. Create the candidate implementation under engineering change control.
3. Export or manually declare reference and candidate topology in a JSON manifest.
4. Choose and document units, absolute and relative tolerances, the comparison formula and their basis before reviewing results.
5. Run `opensees-migrationkit validate <manifest>`.
6. Investigate every structured difference; do not hide mismatches by changing expectations or tolerances.
7. Retain the exact manifest, JSON audit report and any CSV differences. When automated checks pass, review the evidence as a qualified engineer.
8. Record human approval separately, with reviewer identity and rationale, only after that review.

Future adapters may automate step 3. Future execution support may add solver-level evidence, but those extensions must preserve the same discrepancy and approval boundaries.

Keep automatic results separate from engineering recommendations. A failed check remains visible even if a human documents an acceptable residual for a limited purpose. Missing definitions or unverified response semantics are not a numerical pass. The current automated lifecycle and manual approval API provide no failed-check waiver.

Source labels in the manifest are not extraction evidence. Record actual source/run provenance outside the core when producing declared data; the core itself fingerprints only the manifest it reads. See [manifest and reports](manifest_and_reports.md) and [future adapter requirements](future_adapters.md).
