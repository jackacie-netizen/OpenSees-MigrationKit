# Minimal elastic 2D portal

This synthetic benchmark was created from scratch for OpenSees-MigrationKit. It represents a one-bay, one-storey elastic frame with four nodes and three elements.

The Tcl and Python files are transparent reference artifacts showing the same intended topology. Version 0.1.1 does not execute them. Instead, the manifest declares reference and candidate data explicitly and the CLI compares those declarations:

```console
opensees-migrationkit validate benchmarks/minimal_portal/manifest.json \
  --json-report build/minimal-portal-report.json \
  --csv-report build/minimal-portal-differences.csv
```

A passing comparison advances only to `ENGINEER_REVIEW`. It is not proof of solver equivalence or engineering approval.
