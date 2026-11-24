# NexOS

**A persistent operating environment for human and agent work.**

NexOS makes workspaces, bounded delegation, recoverable execution and inspectable effects first-class resources. People can use ordinary applications, manipulate state directly, compose typed capabilities or delegate to a model-driven agent within the same work context.

The reference direction is upstream Linux with a portable user-space runtime. NixOS supplies the initial reproducible qualification VM and a later reference distribution. The first product is a useful managed project workspace; the long-term architecture also supports generated interfaces, reusable procedures, federated compute and separately qualified physical-system adapters.

## What is in this repository

This is an engineering specification and execution program, **not an implemented OS**. Included executable code checks the specification itself: schemas, examples, dependency graph, requirement coverage, evidence-record shape and documentation references. It does not implement a `nexos` runtime or claim that a VM, model, provider or security boundary has been tested.

| Area | Start here |
| --- | --- |
| Vision and value beyond AI | [Vision](docs/VISION.md), [opportunity costs](docs/OPPORTUNITY-COSTS.md) |
| Product and interaction | [Product design](docs/PRODUCT-DESIGN.md), [ten experiences](docs/USER-EXPERIENCE.md) |
| Actual AI-native behavior | [AI-native runtime](docs/AI-NATIVE.md) |
| Requirements and document ownership | [Constitution](docs/CONSTITUTION.md), [specification rules](docs/SPECIFICATION.md) |
| Architecture and recovery | [Architecture](docs/ARCHITECTURE.md), [state and recovery](docs/STATE-AND-RECOVERY.md), [platform](docs/PLATFORM.md) |
| Authority and protocols | [Security](docs/SECURITY.md), [ontology](docs/ONTOLOGY.md), [protocols](docs/PROTOCOLS.md) |
| Machine-readable contracts | [Contract registry](contracts/README.md) |
| Existing RobotMind integration | [Verified source discovery and remaining gates](docs/INTEGRATION.md) |
| Engineering sessions | [AGENTS.md](AGENTS.md), [start mandate](program/START-HERE.md), [execution procedure](program/EXECUTION.md) |
| Program and acceptance | [Program](program/PROGRAM.md), [plan](program/plan.json), [state](program/state.json), [conformance](conformance/ACCEPTANCE.md) |
| Review findings, in Spanish | [Exhaustive proposal review](audits/REVIEW-2026-11-24.es.md) |
| Primary technical sources | [Source register](docs/SOURCES.md) |

## First integrated result

Create a managed workspace, run a real typed operation under bounded authority, inspect its receipts, branch managed state, validate/promote a change, interrupt/recover a task and resume from a persistent shell. Core use remains available with inference disabled. A separate AI milestone adds a real model, authorized context, adaptive plans and independently verified outcomes.

This delivers a concrete product while preserving the wider vision. Generated views, demonstration learning, reference-image lifecycle, federation and accelerated hardware extend independently qualified profiles. They are not all prerequisites for a local-runtime release.

## Verify this package

From the repository root:

```bash
python3 -m pip install -r requirements-spec.txt
python3 scripts/validate_spec.py --report evidence/spec-validation.json
python3 -m unittest discover -s scripts/tests -v
```

The checked-in report records the inputs checked and tool versions. Re-run it after edits. The 15 engineering packages and seven release profiles remain pending; successful specification checks do not change those states.

## Begin implementation

Use [the bounded M1 mandate](program/START-HERE.md), then [AGENTS.md](AGENTS.md). P00 resolves the actual target pins and the first integration contract. P01 immediately exercises a real operation rather than delivering empty services. Continue through the assigned milestone without stopping at each commit; preserve exact checkpoints when a session must end.

The first qualification target is a CPU-only x86_64 Linux/KVM/QEMU environment with a NixOS guest and explicitly managed storage. P00 records actual versions, image hashes, host features and limits. No fictitious release pin, hardware-support promise or boot evidence is supplied here.

## Project status and licensing

Specification version `0.1.0`, reviewed 2026-11-24. Architecture decisions are proposed implementation defaults with measured revisit gates. The target repository name is `robotmindio/nexos`; this archive has not created or published it. Licensing and public distribution remain owner-selected decisions. No license grant or release approval is invented by this package, and those decisions do not block ordinary local engineering.
