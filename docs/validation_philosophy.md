# Validation philosophy

Migration validation should make assumptions and discrepancies inspectable. A successful translation is not established by similar-looking source files.

Version 0.1.0 follows four principles:

1. **Explicit inputs.** Reference and candidate topology are declared in a versioned JSON manifest.
2. **Literal tolerances.** Absolute and relative tolerances are supplied by the user and applied without automatic relaxation.
3. **Structured discrepancies.** Missing IDs, coordinate changes, connectivity changes, and numerical differences are retained as machine-readable records.
4. **Human engineering authority.** Automated success advances to `ENGINEER_REVIEW`, never directly to `APPROVED`.

The tool reports what its implemented comparisons establish. It does not infer mechanical equivalence, solver equivalence, or structural safety from a topology match.
