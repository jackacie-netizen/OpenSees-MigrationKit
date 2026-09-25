# Phase 1 Clean-Room Repository Design

## Purpose

Create `OpenSees-MigrationKit` v0.1.0 as a publication-safe, independent Python project. It provides a deterministic manifest-driven validation core for comparing explicitly declared reference and candidate structural-model topology and numerical data. It is not an automatic Tcl-to-Python translator or a solver runner.

## Provenance boundary

The private research project is read-only and supplies domain context only. No code, model geometry, constants, results, prose, files, or Git history are copied from it. Every public implementation file and benchmark is written from scratch. The synthetic benchmark is a small, generic, one-bay one-storey 2D elastic portal frame.

## Architecture

The package uses a `src/` layout and Python's standard library at runtime.

- `manifest.py` parses and validates JSON into immutable model data objects.
- `tolerances.py` implements explicit absolute/relative comparisons without tolerance relaxation.
- `topology.py` compares node IDs, coordinates, element IDs, and connectivity and returns structured differences.
- `comparison.py` combines topology and scalar numerical comparisons into an overall result.
- `validation_state.py` enforces the automated lifecycle and isolates manual approval behind a separate API requiring reviewer identity and an approval note.
- `reporting.py` serializes deterministic JSON reports and flat CSV difference rows.
- `cli.py` implements `opensees-migrationkit validate <manifest>` and never invokes the human-approval API.

Future adapters may construct the same manifest/model objects, but v0.1.0 contains no Tcl execution, OpenSeesPy execution, topology extraction, dual-run orchestration, response comparison, equilibrium checks, or modal comparison.

## Manifest and data flow

The JSON document contains `schema_version`, `project`, `tcl_source`, `python_target`, `units`, `tolerances`, `reference`, `candidate`, and `validation_state`. Each topology has `nodes` keyed by stringified integer ID and `elements` keyed by stringified integer ID. A node value is a coordinate list; an element value contains a `connectivity` list. Optional `numerical_values` maps named quantities to finite numbers on each side.

The CLI loads the manifest, marks the in-memory run `RUNNING`, performs comparisons, transitions to `FAILED` or `PASSED_AUTOMATED_CHECKS`, advances successful runs to `ENGINEER_REVIEW`, writes requested JSON/CSV reports, prints a concise summary, and returns exit code 0 for a passing automated comparison or 1 for validation failure/input errors.

## Lifecycle policy

Ordinary transitions permit only:

`NOT_RUN -> RUNNING -> FAILED | PASSED_AUTOMATED_CHECKS -> ENGINEER_REVIEW`

`APPROVED` is rejected by the automated transition method. A separate `record_human_approval` API requires a non-empty reviewer identifier and note, starts only from `ENGINEER_REVIEW`, and records `manual_initiation: true`. It is neither imported nor called by the validation CLI.

## Error handling

Manifest errors identify the invalid field and fail closed. IDs must be integers represented as JSON object keys, coordinates/connectivity must be non-empty arrays of the appropriate finite numeric/integer type, tolerances must be finite and non-negative, and numerical comparison rejects non-finite values. Reports are written only after validation has produced a complete result.

## Testing and verification

Pytest covers manifest parsing and malformed input, matching topology, missing/extra nodes and elements, coordinate mismatch, connectivity mismatch, absolute and relative tolerance boundaries, structured reports, CSV output, lifecycle transitions, blocked automated approval, required manual reviewer metadata, and CLI pass/fail behavior. CI runs the same core suite on Python 3.10, 3.11, and 3.12 without proprietary dependencies.

Release verification includes editable installation, CLI help, the synthetic benchmark manifest, repository-wide privacy scanning, Git status, and local Git history inspection. No GitHub remote is created.

## Documentation and claims

README and supporting documents distinguish implemented manifest-driven comparison from planned execution and response-level capabilities. They state that automated checks are not engineering approval, identify the project as independent from OpenSees, include the required early-stage disclaimer, and use the BSD 3-Clause License under Jackie Chen for 2026.
