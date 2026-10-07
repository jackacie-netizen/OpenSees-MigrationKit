# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-10-07

### Fixed

- Reject duplicate JSON keys, unsupported manifest schema versions and unknown fields instead of silently discarding data.
- Reject element connectivity that references undeclared nodes in either topology.
- Reject unsupported tolerance policies in both manifest and programmatic comparisons.

### Added

- JSON report schema 1.1: loaded manifest SHA-256 and byte size, source labels, package version, units, tolerance policy, comparison scope and validation transition history.
- Portable manual approval history including reviewer, note and manual-initiation flag.
- Documentation for input schema, audit evidence, threshold provenance, residual review and future response-adapter requirements.
- Regression coverage for input integrity, audit export and preservation of failed checks.

### Compatibility

- Manifest schema remains 1.0. Existing documented manifests remain valid; an optional `tolerances.policy` may explicitly select `symmetric_max`.
- The existing symmetric-max tolerance calculation, CSV difference columns and automated lifecycle are unchanged.
- JSON consumers must accept report schema 1.1 and its additional fields. Previously ignored fields and malformed connectivity now fail validation.

## [0.1.0] - 2026-09-25

### Added

- Strict JSON manifest parsing for declared model data.
- Node, coordinate, element, and connectivity comparison.
- Absolute and relative numerical tolerance comparison.
- Structured JSON and CSV reports.
- Automated validation lifecycle through `ENGINEER_REVIEW` with a separate manual approval API.
- Command-line manifest validation.
- Synthetic minimal elastic 2D portal benchmark.
- Python 3.10-3.12 test workflow.
