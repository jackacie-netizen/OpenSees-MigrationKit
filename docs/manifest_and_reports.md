# Manifest and report contract

Version 0.1.1 accepts manifest schema `1.0` and emits JSON report schema `1.1`. Package, manifest and report versions describe different interfaces.

## Input contract

The manifest is UTF-8 JSON. Duplicate object keys are invalid at every nesting level. Unknown fields in fixed-shape objects are rejected, so a field cannot silently appear to have been validated. Unsupported schema versions are rejected.

| Object | Fields |
| --- | --- |
| Manifest | Required: `schema_version`, `project`, `tcl_source`, `python_target`, `units`, `tolerances`, `reference`, `candidate`, `validation_state`. |
| Tolerances | Required nonnegative finite numbers: `absolute`, `relative`. Optional: `policy`. |
| Reference or candidate | Required: `nodes`, `elements`. Optional: `numerical_values` (defaults to an empty object). |
| Element | Required: `connectivity`, an ordered nonempty array of integer node IDs. Each node must be declared in the same topology. |
| Nodes | Canonical stringified integer IDs mapped to nonempty arrays of finite coordinates. Boolean values are not numbers. |
| Numerical values | User-defined nonempty names mapped to finite scalar numbers. |
| Units | User-defined nonempty names mapped to nonempty unit labels. |

Project and source labels must be nonempty strings. Source labels are descriptive metadata; the core does not open model files. Units must already be consistent between reference and candidate. The parser does not verify dimensional consistency, expected engineering coverage, material definitions or coordinate-system semantics. An empty comparison covers no objects, even if it reports a pass.

The CLI requires `validation_state` to be `NOT_RUN`. Other recognized state labels can be read by the parser, but cannot authorize a CLI approval or bypass the automated lifecycle.

The checked-in [portal manifest](../benchmarks/minimal_portal/manifest.json) is a complete example. Material properties, loads, constraints and solver settings are not topology fields in schema 1.0. Do not add them as unchecked element fields. A named scalar comparison may compare a declared number, but does not verify its derivation or constitutive meaning.

## Tolerance policy

The only supported policy is `symmetric_max`. Omitting `policy` preserves the v0.1.0 behavior. An unsupported policy fails rather than falling back silently.

```text
abs(candidate - reference) <= max(absolute, relative * max(abs(reference), abs(candidate)))
```

For example, reference `10`, candidate `11.5`, absolute `1` and relative `0.1` fail: the difference is `1.5`, whereas the limit is `1.15`. A different rule, `absolute + relative * abs(reference)`, would yield `2` and pass. That additive rule is not implemented here. Preserve the selected formula when exchanging QA profiles; labels such as "relative tolerance" alone are insufficient.

The single tolerance configuration applies to every coordinate and named scalar. For quantities with different dimensions or required cutoffs, prepare separate manifests with the appropriate units and tolerances. Per-quantity profiles are not implemented. Neither thresholds nor source data are adjusted to obtain a pass.

## JSON report 1.1

The existing result fields remain: `schema_version`, `project`, `passed`, `validation_state`, `summary`, `differences`. The report now also carries:

| Field | Meaning |
| --- | --- |
| `provenance` | Package version, input schema version, loaded manifest SHA-256 and byte size, declared Tcl/Python source labels. |
| `units` | The manifest's unit labels. |
| `tolerances` | Absolute and relative values and explicit policy. |
| `comparison_scope` | Checked fields and explicit flags that solver execution and source-artifact verification were not performed. |
| `validation_history` | Ordered transitions, actor, note and manual-initiation flag. |

The fingerprint is computed from the bytes read once during manifest loading. Whitespace changes produce a different fingerprint. Later edits to the input file do not change the identity attached to that loaded object. Programmatically constructed `Manifest` objects may have `null` fingerprint/size; the report must not invent file provenance for them.

The fingerprint identifies the input manifest, not the Tcl/Python files, an executable, a run or the origin of the declared values. Retain the original manifest alongside the report. No current timestamp or absolute local path is added automatically, so identical inputs and lifecycle records produce deterministic JSON.

`passed` applies only to declared comparisons. It does not establish complete model coverage, mechanical equivalence, successful solver execution or engineering approval. A failed comparison produces `FAILED` and preserves its differences. Invalid input returns a nonzero CLI status without creating a new validation report. Use distinct output paths for each run: an older file at the requested destination is not evidence of a failed invocation's result.

An authorized human application can export the separately recorded approval event through `build_report`. The ordinary `validate` CLI cannot create that event. The API records the supplied reviewer declaration; it provides neither authentication nor a tamper-proof signature.

## CSV and compatibility

CSV retains its six difference columns: `category`, `identifier`, `field`, `reference`, `candidate`, `message`. A matching comparison has only the CSV header. CSV alone is not a complete audit record.

Documented schema-1.0 manifests remain usable. Inputs relying on duplicate keys, ignored fields or dangling connectivity are intentionally rejected. JSON consumers must accept report schema 1.1 and the additional audit fields; this is a visible output-contract revision, not a silent claim of schema-1.0 compatibility.
