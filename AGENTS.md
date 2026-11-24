# NexOS engineering instructions

## Mandate and scope

Develop the capabilities defined by the canonical specification. This repository currently contains a design and engineering program, not an operational OS. A schema, generated screen, successful build or passing specification validator is not evidence that runtime behavior exists.

The owner assigns a bounded scope: packages or milestone, target environment, permitted repositories and external actions, resource ceiling and any deadline. Carry that scope through implementation, integration, debugging, simplification and qualification. Continue between commits and intermediate milestones while authorized work remains. The roadmap does not grant an unbounded mandate to execute every future package, incur unlimited cost, publish or operate physical equipment.

Existing authorization persists across sessions. Do not request it again for routine edits, local experiments, inspection, tests, fixes or actions clearly included in the mandate. A missing optional integration must not halt unrelated work. Escalate only an actual authority, access, resource or conflicting-requirement decision, after preparing concrete options and identifying the affected acceptance criteria.

## Start and resume

1. Read [README](README.md), the constitution, architecture and assigned package. Read applicable contracts, ADRs, experience specifications and invariants before changing their behavior. Avoid loading every historical log.
2. Reconcile [plan.json](program/plan.json), [state.json](program/state.json), Git HEAD, the worktree and the latest checkpoint. Records support continuity; inspect actual files and processes to confirm them.
3. Establish base revision, owned paths, dependencies, target tuple and acceptance commands. If implementation is absent, implement the first real path; do not manufacture a pass record.
4. Claim disjoint work through [EXECUTION.md](program/EXECUTION.md). A JSON lease field or Git commit is not an atomic distributed lock. Without a real atomic coordinator, one coordinator assigns ownership and serializes integration.
5. Resume the checkpoint's next concrete action. Check whether previously launched commands or external operations remain active before reissuing them.

## Implementation rules

- Deliver observable vertical behavior. P01 already executes a real bounded local operation through admission and effect recording; subsequent work strengthens and extends it.
- Keep one canonical owner for authority, admission accounting and operational state. A module boundary does not justify another daemon. Prefer the specified modular runtime, narrow helper and isolated workers.
- Inspect the smallest relevant RobotMind surface at a pinned revision. Reuse or extend suitable existing contracts; document a measured mismatch before rejecting them. Never create a second Bifrost or a parallel generic workflow engine. Existing discovery evidence is recorded in [INTEGRATION.md](docs/INTEGRATION.md); it is not integration qualification.
- Preserve local deterministic bootstrap without optional remote services. A bounded local task journal supports offline recovery; it is not a reason to clone distributed orchestration.
- Models and generated UI are untrusted request producers. Deterministic policy and OS enforcement decide authority. Model confidence, a visible UI control or retrieved instructions cannot grant permission.
- Preserve guarantee scope: managed resources versus host state; recorded provenance versus inferred explanation; idempotency versus universal exactly-once execution; compensating recovery versus universal rollback.
- Maintain one canonical contract per concept. Incompatible semantic changes need an ADR, migration and affected acceptance updates. Avoid speculative abstractions and duplicate compatibility paths.
- Unit tests, contract fixtures and design simulations may use doubles when labeled. Product qualification uses the actual substrate and declared provider. A fixture, screenshot or fabricated trace is never integration evidence.
- Do not weaken a failing assertion or broaden threat-model exclusions to obtain a pass. Record an agreed scope change explicitly.

## Work loop and collaboration

Select an unblocked package within the mandate; implement the next integrated acceptance path; run checks that resolve its concrete risks; fix failures; then cover its failure and recovery paths. Keep schemas, examples, UX, behavior and documentation consistent. Delete superseded paths after a tested migration.

Delegate disjoint work or independent review when useful. Assign an owner, path scope, contract revision and output expectation. Use separate worktrees for concurrent implementation. Shared contracts have one active editor or an agreed change proposal. The integration owner combines changes against a known head and reruns affected checks. Independent qualification belongs at package and release-profile boundaries, without a review queue for every edit.

Do not repeat a failing attempt indefinitely without new evidence. Record hypotheses, change the method or conduct a bounded spike. If an external blocker persists, checkpoint it and continue an independent authorized package. Hardware unavailable for a hardware claim cannot be replaced by emulation while retaining that claim.

## Evidence, checkpoints and completion

Follow [ACCEPTANCE.md](conformance/ACCEPTANCE.md). The author may mark a package `implemented` when work and evidence are ready. `qualified` requires independent reproduction against the exact submitted revision and environment. If a verifier is unavailable, leave it `implemented`; continue work that does not require its unqualified security guarantees.

Failures invalidate affected claims, not unrelated packages. Preserve negative evidence and dependency impact. After a change, rerun checks affected by it instead of reflexively repeating the whole suite. Every release profile states exactly what it qualifies.

Checkpoint before session exhaustion, context loss, handoff or ownership transfer. Record worktree/branch, base/head, uncommitted patch reference, command/process states, environment, actual checks, evidence digests, decisions, blockers, lease/fencing and the next action. Keep secrets out. Commits are useful checkpoints; session completion is not program completion.

Report what works, its evidence, exclusions and how work resumes. Distinguish specification validation, implementation, integration and independent qualification.
