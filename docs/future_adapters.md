# Future adapter requirements

These requirements guide planned Tcl/OpenSeesPy execution and response comparison. Version 0.1.1 implements none of those adapters, solver runs or response-level checks.

## Baseline and procedure identity

Identify the designated baseline, source revision and solver build before comparing outputs. Keep literal baseline reproduction, authorized corrections and experimental model variants distinguishable. An inherited modeling concern must be documented independently from a demonstrated translation error. Do not tune model parameters, integration or convergence settings to stored regression observations.

A future run record should identify sources and binaries by hashes, units, active procedure, loads, constraints, solver settings, recorder inventory and authorized scope. Approval for one phase does not imply authorization for later analyses.

## Response semantics and coverage

Record which outputs represent committed states and which are failed attempts or diagnostics. Preserve return codes, recovery attempts, valid final time and completion status. An incomplete run cannot supply full-record conclusions. Do not fill missing response tails, residual metrics or undefined quantities with invented values.

Compare the same physical quantity on corresponding members, ends, axes, units and response components. Extra members in one system must not silently enter a matched-member comparison. Distinguish local, basic and global forces, and verify mappings against the relevant element formulation and installed solver version. Establish recorder versus direct-query agreement at the same state before interpreting cross-engine discrepancies.

Comparisons across response suites must identify the common completed-record set. Partial-record peaks may be reported with their valid time coverage, but must stay distinguishable from full-record peaks. Retain controlling member, component, end, signed value, record and time where appropriate.

## Numerical and engineering findings

Declare QA formulas and thresholds before examining results, with their units, source and scope. Preserve the numerical result separately from reporting filters and engineering disposition. A failed QA screen stays failed even if an engineer accepts a documented residual for a specified use.

Report actual equilibrium residuals with the balance definition, participating load path and available force/inertia/damping terms. Do not invent a universal acceptance cutoff. Nonconvergence alone does not prove collapse; matching periods or peaks alone do not establish all-channel equivalence. Different iteration counts are diagnostic evidence rather than a universal equivalence gate.

Classifying a difference as floating point, sampling or component mapping requires evidence for that mechanism. Otherwise keep the cause unresolved. Human review should assess consequences for the stated engineering use and preserve unresolved questions and excluded coverage.

## Publication and verification

Implement adapters only with focused tests and publication-safe synthetic examples. Keep private models, parameters, ground motions, outputs and manuscript content outside this repository. Capability status may change to Implemented only after the relevant execution and comparison behavior exists and has been verified.
