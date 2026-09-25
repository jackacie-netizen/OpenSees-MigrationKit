# OpenSees-MigrationKit

> A research-grade open-source toolkit for migrating and validating OpenSees Tcl models against OpenSeesPy implementations.

OpenSees-MigrationKit v0.1.0 provides a deterministic, manifest-driven validation core for comparing structural model topology and numerical data. Direct Tcl/OpenSeesPy execution and response-level equivalence testing are planned extensions.

**Status:** Early-stage public research tooling; APIs and validation coverage are still evolving.

Many engineering and research workflows contain legacy OpenSees Tcl models while newer workflows increasingly use Python and OpenSeesPy. Translation alone is insufficient: scripts that appear equivalent can create different nodes, connectivity, or numerical data. This project makes declared comparisons reproducible, discrepancies explicit, and engineering review traceable.

OpenSees-MigrationKit is an independent project and is not affiliated with or endorsed by the official OpenSees project.

## Current capabilities

| Capability | Status |
| --- | --- |
| JSON manifest parsing and validation | Implemented |
| Node ID and coordinate comparison | Implemented |
| Element ID and connectivity comparison | Implemented |
| Explicit absolute and relative numerical tolerances | Implemented |
| Structured differences and deterministic JSON/CSV reports | Implemented |
| Regression tests and a synthetic portal benchmark | Implemented |
| Validation lifecycle with a human approval boundary | Implemented |
| CLI validation of manifest-provided data | Implemented |
| Direct Tcl execution or topology extraction | Planned |
| Direct OpenSeesPy execution or topology extraction | Planned |
| Tcl/OpenSeesPy dual-run orchestration | Planned |
| Force-equilibrium and recorder-response validation | Planned |
| Eigenvalue, period, and nonlinear-response comparison | Planned |

Version 0.1.0 is the foundational validation layer for a larger migration workflow. It is not a complete automatic migration engine and does not establish engineering correctness.

## Installation

Python 3.10 or newer is required.

```console
python -m pip install -e .
```

For development:

```console
python -m pip install -e ".[dev]"
python -m pytest -v
```

## Quick start

Validate the included synthetic benchmark and write both report formats:

```console
opensees-migrationkit validate benchmarks/minimal_portal/manifest.json \
  --json-report build/minimal-portal-report.json \
  --csv-report build/minimal-portal-differences.csv
```

The manifest declares reference and candidate nodes, elements, numerical values, units, and tolerances. A minimal topology section looks like this:

```json
{
  "nodes": {"1": [0.0, 0.0], "2": [4.0, 0.0]},
  "elements": {"1": {"connectivity": [1, 2]}},
  "numerical_values": {"bay_width": 4.0}
}
```

Comparison failures produce structured records identifying the category, model identifier, field, reference value, candidate value, and explanatory message. Configured tolerances are applied literally and are never relaxed automatically.

## Benchmark

[`benchmarks/minimal_portal`](benchmarks/minimal_portal) is a publication-safe one-bay, one-storey elastic 2D portal frame created specifically for this project. Its Tcl and Python files are readable examples; v0.1.0 validates only their explicitly declared manifest data and does not execute either model.

## Validation philosophy and human review

The automated lifecycle is:

```text
NOT_RUN -> RUNNING -> FAILED
                   -> PASSED_AUTOMATED_CHECKS -> ENGINEER_REVIEW
```

Automated software and AI agents cannot assign `APPROVED`. The separately exposed manual approval API requires a human reviewer identifier and approval note and is not reachable through the `validate` CLI. Passing automated tests is evidence about implemented comparisons, not structural-engineering approval.

See [validation philosophy](docs/validation_philosophy.md), [migration workflow](docs/migration_workflow.md), and [engineering review](docs/engineering_review.md).

## Roadmap

Planned work includes adapters for Tcl and OpenSeesPy data extraction, controlled dual-run orchestration, recorder and response comparison, equilibrium checks, modal comparisons, and broader benchmark coverage. Each capability will be documented as implemented only after deterministic tests and public examples exist.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Reports of security concerns should follow [SECURITY.md](SECURITY.md).

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff).

## License

BSD 3-Clause License. See [LICENSE](LICENSE).

## Engineering and research disclaimer

This software assists comparison and recordkeeping. It does not replace verification by a qualified engineer, establish that two solver models are mechanically equivalent, or certify a structure as safe or code-compliant. Users remain responsible for model interpretation, solver configuration, units, boundary conditions, numerical assumptions, and engineering decisions.
