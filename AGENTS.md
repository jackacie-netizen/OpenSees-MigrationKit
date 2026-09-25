# Instructions for AI coding agents

- Treat public manifests and documented fixtures as source-of-truth inputs; never infer missing engineering data.
- Do not copy from private research repositories, unpublished models, or confidential results.
- Never change model values, numerical tolerances, or units silently.
- Never relax a tolerance to convert a discrepancy into a pass.
- Never edit expected results merely to make tests pass; investigate and report the discrepancy.
- Preserve deterministic ordering and structured difference details.
- Automated tests are evidence, not engineering approval.
- Automated agents and normal validation code cannot assign `APPROVED`.
- Keep the human-only approval API separate from automated validation and require reviewer identity plus an approval note.
- Do not claim direct solver execution or response equivalence until those capabilities exist and are tested.
