# Validation philosophy

Migration validation should make assumptions and discrepancies inspectable. A successful translation is not established by similar-looking source files.

Version 0.1.1 follows four principles:

1. **Explicit inputs.** Reference and candidate topology are declared in a versioned JSON manifest.
2. **Literal tolerances.** Absolute and relative tolerances are supplied by the user and applied without automatic relaxation.
3. **Structured discrepancies.** Missing IDs, coordinate changes, connectivity changes, and numerical differences are retained as machine-readable records.
4. **Human engineering authority.** Automated success advances to `ENGINEER_REVIEW`, never directly to `APPROVED`.

The tool reports what its implemented comparisons establish. It does not infer mechanical equivalence, solver equivalence, or structural safety from a topology match.

## Evidence and authority

Name the source baseline before evaluating a migration. Preserve its identity and distinguish any authorized correction or model variant. A migration reproduces the selected definition; improving an inherited physical assumption is an independent engineering decision.

References must support the claim actually made. Solver documentation can establish a response meaning; a publication can support a method; an internal protocol can choose a QA threshold. None of those sources automatically supports every other type of claim. Stored observations are regression evidence, not values to fit by tuning the model.

Do not loosen tolerances after inspecting discrepancies or reinterpret reporting filters as acceptance criteria. Any future protocol change should identify the reason, date and affected scope and preserve previous results.

The JSON report binds a comparison to its loaded manifest bytes and exports lifecycle events. It does not certify the origin or completeness of manually declared data. Preserve the original input and independently verify the engineering coverage that the report cannot establish.
