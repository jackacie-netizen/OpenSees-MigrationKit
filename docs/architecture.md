# Architecture

OpenSees-MigrationKit v0.1.0 separates input parsing, pure comparison, lifecycle policy, reporting, and command-line orchestration.

## Components

- `manifest` converts a strict JSON document into immutable Python data objects.
- `tolerances` performs explicit finite-number comparisons.
- `topology` reports node and element differences without side effects.
- `comparison` aggregates topology and named numerical comparisons.
- `validation_state` enforces automated transitions and isolates manual approval.
- `reporting` serializes complete results to deterministic JSON and CSV.
- `cli` wires these components together for the `validate` command.

The comparison core accepts ordinary typed data rather than solver objects. Future Tcl or OpenSeesPy adapters can therefore produce the same `Topology` and `Manifest` structures without coupling the core to a solver runtime. No speculative adapter framework is included in v0.1.0.

## Data flow

```text
JSON manifest -> strict parser -> immutable manifest
              -> topology/numerical comparison -> structured differences
              -> lifecycle transition -> JSON/CSV report and exit status
```

Input errors fail closed. Differences remain visible; tolerances are never changed by the comparison process.
