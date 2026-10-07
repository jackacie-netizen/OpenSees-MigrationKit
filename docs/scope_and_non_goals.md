# Scope and non-goals

## Version 0.1.1 scope

- Strict JSON manifest parsing.
- Comparison of node IDs and coordinates.
- Comparison of element IDs and ordered connectivity.
- Named finite-number comparison using explicit tolerances.
- Structured JSON and CSV reports.
- A lifecycle that separates automated checks from manual approval.
- A command-line workflow over declared data.
- Duplicate-key, supported-schema, known-field and declared-node-reference enforcement at JSON loading.
- Manifest-byte fingerprint, explicit tolerance policy and lifecycle evidence in JSON reports.

## Non-goals for version 0.1.1

- Running Tcl or Python model scripts.
- Parsing arbitrary Tcl or Python to discover topology.
- Orchestrating two solver runs.
- Comparing recorders, forces, eigenvalues, periods, or nonlinear response.
- Translating engineering model commands automatically.
- Certifying engineering correctness or structural safety.
- Converting units, validating physical dimensions or authenticating human approval.
- Classifying numerical residual causes or waiving failed automated checks.

These boundaries keep the first release deterministic, dependency-light, and honest about what it proves.

Generic response-adapter design requirements are documented in [future adapters](future_adapters.md); those requirements are not implemented validation coverage.
