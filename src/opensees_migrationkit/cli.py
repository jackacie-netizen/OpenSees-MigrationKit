"""Command-line interface for manifest-driven validation."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .comparison import validate_manifest
from .manifest import ManifestError, load_manifest
from .reporting import build_report, write_csv_report, write_json_report
from .validation_state import ValidationRecord, ValidationState, transition_automated


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="opensees-migrationkit",
        description="Validate declared reference and candidate model data.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a JSON manifest")
    validate.add_argument("manifest", help="path to the JSON manifest")
    validate.add_argument("--json-report", help="write a JSON validation report")
    validate.add_argument("--csv-report", help="write a CSV difference report")
    return parser


def _validate(args: argparse.Namespace) -> int:
    try:
        manifest = load_manifest(args.manifest)
        if manifest.validation_state != ValidationState.NOT_RUN.value:
            raise ManifestError("automated validation must start at NOT_RUN")
        record = transition_automated(ValidationRecord(), ValidationState.RUNNING)
        result = validate_manifest(manifest)
        if result.passed:
            record = transition_automated(record, ValidationState.PASSED_AUTOMATED_CHECKS)
            record = transition_automated(record, ValidationState.ENGINEER_REVIEW)
        else:
            record = transition_automated(record, ValidationState.FAILED)
        report = build_report(manifest, result, record)
        if args.json_report:
            write_json_report(args.json_report, report)
        if args.csv_report:
            write_csv_report(args.csv_report, result.differences)
    except (ManifestError, OSError, ValueError) as error:
        print(f"Invalid manifest: {error}", file=sys.stderr)
        return 1

    status = "PASS" if result.passed else "FAIL"
    print(f"{status} state={record.state.value} differences={len(result.differences)}")
    return 0 if result.passed else 1


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate":
        return _validate(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
