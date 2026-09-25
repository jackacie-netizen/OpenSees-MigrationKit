# Phase 1 Clean-Room Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and locally release-check OpenSees-MigrationKit v0.1.0 as a publication-safe manifest-driven topology and numerical validation package.

**Architecture:** Immutable manifest objects feed pure tolerance and topology comparison functions. A small orchestration layer produces deterministic report objects, while the CLI controls automated lifecycle transitions and report files without exposing manual approval.

**Tech Stack:** Python 3.10+, standard library runtime, pytest, setuptools, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-25-phase-1-clean-room-design.md`

## Global Constraints

- Do not modify or copy from the private source repository.
- Do not add OpenSees, OpenSeesPy, Tcl execution, solver execution, or proprietary dependencies.
- Runtime dependencies remain empty; pytest is a development extra.
- Package version and citation version are exactly `0.1.0`.
- Automated validation never assigns `APPROVED`.
- No GitHub remote is created and nothing is pushed.
- Public files must not contain private paths or unpublished research terms/data.

## Review Focus

- Reject booleans where integer IDs or numeric coordinates are expected; Task 1 tests this explicitly.
- Reject NaN and infinity in tolerances, coordinates, and numerical values; Tasks 1 and 2 test this explicitly.
- Treat coordinate dimension mismatch as a failed structured comparison, not an exception; Task 2 tests this explicitly.
- Keep output ordering deterministic across JSON and CSV reports; Task 4 tests this explicitly.
- Ensure the CLI cannot reach or expose manual approval; Task 5 tests its output and parser surface.

---

### Task 1: Package skeleton and manifest model

**Files:**
- Create: `pyproject.toml`, `src/opensees_migrationkit/__init__.py`, `src/opensees_migrationkit/manifest.py`
- Test: `tests/test_manifest.py`

**Interfaces:**
- Produces: `ToleranceConfig`, `Topology`, `Manifest`, `ManifestError`, and `load_manifest(path: str | Path) -> Manifest`.

- [ ] Write manifest tests for a complete JSON fixture, missing keys, invalid ID keys, boolean IDs, empty coordinates/connectivity, non-finite numbers, and negative tolerances.
- [ ] Run `python -m pytest tests/test_manifest.py -v`; expect import failure before implementation.
- [ ] Implement frozen dataclasses and strict parsing helpers. Normalize node and element keys to integers while retaining source/target paths as relative metadata strings.
- [ ] Run `python -m pytest tests/test_manifest.py -v`; expect all manifest tests to pass.
- [ ] Commit with `chore: initialize OpenSees-MigrationKit`.

The parser contract is `load_manifest(path: str | Path) -> Manifest`; the
returned frozen `Manifest` exposes the exact fields listed in the Interfaces
block above.

### Task 2: Numerical and topology comparison core

**Files:**
- Create: `src/opensees_migrationkit/tolerances.py`, `src/opensees_migrationkit/topology.py`, `src/opensees_migrationkit/comparison.py`
- Test: `tests/test_tolerances.py`, `tests/test_topology.py`, `tests/test_comparison.py`

**Interfaces:**
- Consumes: `ToleranceConfig`, `Topology` from Task 1.
- Produces: `numbers_close(reference, candidate, tolerance) -> bool`, `Difference`, `compare_topologies(reference, candidate, tolerance) -> tuple[Difference, ...]`, and `validate_manifest(manifest) -> ValidationResult`.

- [ ] Write tolerance tests covering exact equality, absolute boundary, relative boundary, failure outside both tolerances, zero reference, negative tolerance rejection, and non-finite input rejection.
- [ ] Run `python -m pytest tests/test_tolerances.py -v`; expect import failure.
- [ ] Implement `abs(candidate-reference) <= max(abs_tol, rel_tol * max(abs(reference), abs(candidate)))` with finite, non-negative inputs required.
- [ ] Write topology tests for matching models, missing/extra nodes and elements, coordinate mismatch, dimension mismatch, and ordered connectivity mismatch.
- [ ] Implement sorted, structured differences with `category`, `identifier`, `field`, `reference`, `candidate`, and `message`.
- [ ] Write comparison tests for named numerical values missing on either side and outside tolerance.
- [ ] Implement `ValidationResult(passed, differences, summary)` and aggregate topology plus numerical differences.
- [ ] Run `python -m pytest tests/test_tolerances.py tests/test_topology.py tests/test_comparison.py -v`; expect all tests to pass.
- [ ] Commit with `feat: add topology and numerical validation core`.

### Task 3: Validation lifecycle

**Files:**
- Create: `src/opensees_migrationkit/validation_state.py`
- Test: `tests/test_validation_state.py`

**Interfaces:**
- Produces: `ValidationState`, `ValidationRecord`, `transition_automated(record, target) -> ValidationRecord`, and `record_human_approval(record, reviewer, note) -> ValidationRecord`.

- [ ] Write tests for all permitted automated transitions, invalid skips, any automated transition to `APPROVED`, manual approval from a wrong state, and blank reviewer/note values.
- [ ] Run `python -m pytest tests/test_validation_state.py -v`; expect import failure.
- [ ] Implement immutable records with history entries. `transition_automated` rejects `APPROVED`; `record_human_approval` requires `ENGINEER_REVIEW`, non-empty reviewer/note, and records `manual_initiation=True`.
- [ ] Run `python -m pytest tests/test_validation_state.py -v`; expect all tests to pass.
- [ ] Commit with `test: add migration validation regression suite` after Task 4 adds report regression coverage.

### Task 4: Deterministic JSON/CSV reporting

**Files:**
- Create: `src/opensees_migrationkit/reporting.py`
- Test: `tests/test_reporting.py`

**Interfaces:**
- Consumes: `ValidationResult`, `ValidationRecord`.
- Produces: `build_report(...) -> dict`, `write_json_report(path, report) -> None`, and `write_csv_report(path, differences) -> None`.

- [ ] Write tests asserting the complete JSON shape, stable key/order behavior, parent-directory creation, CSV header, and one flat row per difference.
- [ ] Run `python -m pytest tests/test_reporting.py -v`; expect import failure.
- [ ] Implement UTF-8 JSON with sorted keys and newline termination; implement CSV via `csv.DictWriter` with deterministic difference order and JSON-encoded complex cell values.
- [ ] Run `python -m pytest tests/test_reporting.py -v`; expect all tests to pass.
- [ ] Run `python -m pytest -v`; expect all core tests through Task 4 to pass.
- [ ] Commit lifecycle and report tests with `test: add migration validation regression suite`.

### Task 5: CLI and synthetic benchmark

**Files:**
- Create: `src/opensees_migrationkit/cli.py`, `tests/test_cli.py`
- Create: `benchmarks/minimal_portal/model.tcl`, `model.py`, `manifest.json`, `expected_topology.json`, `README.md`
- Create: `benchmarks/README.md`, `examples/README.md`

**Interfaces:**
- Consumes: all earlier public functions.
- Produces: console script `opensees-migrationkit` and subcommand `validate MANIFEST [--json-report PATH] [--csv-report PATH]`.

- [ ] Write CLI tests for help, passing benchmark validation, failing manifest comparison, report creation, invalid JSON, and absence of an approval command.
- [ ] Run `python -m pytest tests/test_cli.py -v`; expect failure before implementation.
- [ ] Implement argparse validation flow with automated lifecycle only, concise stdout/stderr, and exit codes 0 for pass and 1 for validation/input failure.
- [ ] Write the generic portal examples independently in Tcl and Python, plus a manifest whose declared reference/candidate topology matches.
- [ ] Run `python -m pytest tests/test_cli.py -v`; expect all tests to pass.
- [ ] Run `python -m opensees_migrationkit.cli validate benchmarks/minimal_portal/manifest.json`; expect PASS and `ENGINEER_REVIEW`.
- [ ] Commit with `feat: add topology and numerical validation core` if not already committed, keeping CLI with the core feature commit.

### Task 6: Public documentation, policy, and CI

**Files:**
- Create: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, `AGENTS.md`, `CHANGELOG.md`, `.gitignore`, `.editorconfig`
- Create: `docs/architecture.md`, `docs/validation_philosophy.md`, `docs/scope_and_non_goals.md`, `docs/migration_workflow.md`, `docs/engineering_review.md`, `docs/provenance_audit.md`
- Create: `.github/workflows/tests.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/pull_request_template.md`

**Interfaces:**
- Documents the exact public API/CLI and implemented-versus-planned capability matrix.

- [ ] Write public documentation stating the independent-project status, BSD 3-Clause license, human review boundary, benchmark provenance, early-stage disclaimer, and exact v0.1.0 limitations.
- [ ] Add CI using checkout/setup-python and `python -m pip install -e .[dev]`, then `python -m pytest -v` on Python 3.10, 3.11, and 3.12.
- [ ] Verify `README.md`, `pyproject.toml`, `CITATION.cff`, and `CHANGELOG.md` all state version/license consistently.
- [ ] Commit documentation with `docs: add validation and engineering review guidance`.
- [ ] Commit workflow/templates with `ci: add Python test workflow`.

### Task 7: Release verification, privacy audit, and local Git handoff

**Files:**
- Inspect: entire repository and generated Git history.

**Interfaces:**
- Produces: a clean local repository on branch `main` with no configured remotes.

- [ ] Create an isolated virtual environment and run `python -m pip install -e .`.
- [ ] Run `python -m pytest -v` and record passed/failed/skipped totals.
- [ ] Run `opensees-migrationkit --help` and the benchmark validation command.
- [ ] Search tracked and untracked files for forbidden research terms, private paths, secrets, private URLs, key material, and suspicious binary/archive extensions; inspect every hit and remove unsafe content rather than allowlisting it casually.
- [ ] Initialize a new Git repository with branch `main`; create the five truthful logical commits described in the project brief without importing any prior history.
- [ ] Run `git status`, `git log --oneline --decorate -10`, `git remote -v`, and a history-wide privacy scan.
- [ ] Copy the verified repository to the user-requested public-project directory, verify checksums/file counts, and rerun tests from the final location.
- [ ] Confirm no remote exists and report `PUBLICATION_CANDIDATE_READY_FOR_HUMAN_REVIEW` only if all checks pass.
