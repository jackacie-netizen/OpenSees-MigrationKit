# Scope and non-goals

## Version 0.1.0 scope

- Strict JSON manifest parsing.
- Comparison of node IDs and coordinates.
- Comparison of element IDs and ordered connectivity.
- Named finite-number comparison using explicit tolerances.
- Structured JSON and CSV reports.
- A lifecycle that separates automated checks from manual approval.
- A command-line workflow over declared data.

## Non-goals for version 0.1.0

- Running Tcl or Python model scripts.
- Parsing arbitrary Tcl or Python to discover topology.
- Orchestrating two solver runs.
- Comparing recorders, forces, eigenvalues, periods, or nonlinear response.
- Translating engineering model commands automatically.
- Certifying engineering correctness or structural safety.

These boundaries keep the first release deterministic, dependency-light, and honest about what it proves.
