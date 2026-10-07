# Architecture

OpenSees-MigrationKit v0.1.1 separates input parsing, pure comparison, lifecycle policy, reporting, and command-line orchestration.

## Components

- `manifest` checks schema, duplicate keys, field coverage and node references, then retains the loaded input fingerprint in immutable Python data objects.
- `tolerances` performs explicit finite-number comparisons.
- `topology` reports node and element differences without side effects.
- `comparison` aggregates topology and named numerical comparisons.
- `validation_state` enforces automated transitions and isolates manual approval.
- `reporting` serializes comparison results and input/lifecycle evidence to deterministic JSON; CSV contains differences only.
- `cli` wires these components together for the `validate` command.

The comparison core accepts ordinary typed data rather than solver objects. Future Tcl or OpenSeesPy adapters can therefore produce the same `Topology` and `Manifest` structures without coupling the core to a solver runtime. No speculative adapter framework is included in v0.1.1.

## Data flow

```text
JSON manifest -> strict parser -> immutable manifest
              -> topology/numerical comparison -> structured differences
              -> lifecycle transition -> JSON/CSV report and exit status
```

Input errors fail closed. Differences remain visible; tolerances are never changed by the comparison process.

The JSON loader is the input-integrity boundary. Direct dataclass construction and pure comparison APIs assume caller-supplied typed data; they do not repeat all loader checks or prove file provenance. The tolerance function still rejects unsupported policy names. Report fingerprints are captured by the loader, not obtained by reopening source labels during reporting.

Report schema 1.1 and manifest schema 1.0 are intentionally separate contracts. See [manifest and reports](manifest_and_reports.md) for their fields and compatibility rules.
