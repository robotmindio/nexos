# Long-session execution and continuity

Status: normative engineering procedure. It governs agents building NexOS; it does not assert that NexOS already provides a coordinator.

## 1. Concrete mandate

Retain the assigned packages or milestone, owner, allowed repositories/environments, target tuple, resource envelope, external actions and stopping boundary. Ordinary local implementation and verification follow the user's assigned scope. Spending, publishing, external deployment and physical effects follow actual existing authorization; do not ask for that authorization repeatedly.

The scope is finite and completion is reviewable. A session may span packages; a package may span sessions. Token exhaustion and commits do not change acceptance. If no paid-provider budget is authorized, develop deterministic paths and prepare the real-model qualification recipe; mark that qualification blocked instead of simulating it as a pass.

## 2. Canonical records

| Record | Role |
|---|---|
| `plan.json` | Package graph, milestone membership, document and coverage references. No mutable status. |
| `state.json` | Current engineering state, revision, claims, checkpoint/evidence references and blockers. |
| Package Markdown | Scope, implementation boundaries and acceptance detail; dependency IDs in the graph are authoritative. |
| `conformance/matrix.json` | Experience/invariant/package coverage index, validated in both directions. |
| Checkpoint | Immutable handoff of actual working state; state points to the latest record. |
| Evidence | Actual commands, environment, results, artifacts and qualification. |

External trackers may project these records but cannot silently become a second mutable authority. The initial state has no active lease and no runtime qualification. Top-level `qualification` accepts `not_started`, `in_progress` or `partial`: it tracks qualification activity and the presence of scoped results, never global OS completion. Actual claims remain in package/profile records.

The [mandate template](mandate-template.json) and [checkpoint template](checkpoint-template.json) make missing handoff fields visible. They are `template: true`, `active: false`, contain no invented identities or hashes, and cannot be used as active authority, a live lease or runtime evidence. Null means unresolved, not unlimited authority. Completed handoffs must preserve the observed information required below; the template path itself is rejected as an active checkpoint reference. [program.schema.json](../contracts/program.schema.json) validates the current metadata, inactive templates and completed `mandate`/`checkpoint` records.

To instantiate a mandate, copy the template to a new record, use `kind: engineering_mandate`, `template: false`, `active: true`, and fill the observed mandate ID, owner, finite scope, target environment, allowed roots and actual authorized actions with their authority references. Unspecified token/deadline limits are permissible only within the finite assigned scope and known action authority; null never authorizes paid or external work. Resolve package/milestone/profile IDs against the current plan.

To instantiate a checkpoint, use `kind: engineering_checkpoint`, `template: false`, `active: true` in a new record. Fill the observed ID/time, mandate reference, finite scope, actual worktree/base/head, environment-tuple reference, work status, coordination mode and concrete next action. For a dirty worktree, preserve a real patch and digest; for a clean tree, set `uncommitted_patch` to null. A detached HEAD may have a null branch name. State points to this completed record, never the template. Validate it against the `checkpoint` definition and inspect the referenced bytes/state on resume.

In these records `active: true` means the template has been completed as metadata. It does not establish a live process, acquire a claim, renew a lease, grant authority, prove a test result or supersede later revocation. The coordinator and actual execution environment remain authoritative.

## 3. Engineering states

Normal sequence: `pending → in_progress → implemented → qualified`. `blocked` preserves a prior state plus a concrete external or technical obstacle; resolution returns work to that state. Regressions reopen affected work with the failed evidence preserved.

`implemented` means the author supplies completed work and acceptance evidence. It does not authorize consumers to rely on an unqualified security boundary. Downstream non-sensitive implementation may proceed against the contract while review is pending; release qualification may not.

State changes use an expected revision and increment it once when accepted. In a serial repository workflow this is a coordinator convention verified against HEAD, not a database CAS guarantee. A hosted coordinator must enforce comparison atomically in its own store.

## 4. Claims and parallelism

For one worker, an explicit assignment and isolated worktree suffice. For multiple workers, a single coordinator may grant disjoint ownership and serialize merges; alternatively use an existing atomic claim store. Across hosts, use an existing durable coordinator with atomic claim/renew/release semantics. Do not invent another distributed lock service to start this program.

A claim identifies packages, path scope, holder, unique claim ID, issue/expiry times and a monotonically increasing fence. Renewal proves current ownership. Expired holders stop writing and preserve their work. Integration checks the current holder and fence. Timestamp expiry alone cannot prevent a stale process from writing.

Workers use separate branches/worktrees. Shared contracts have one editor or a coordinated proposal. Review operates on a pinned commit. Never reset or clean another worker's tree. Expired ownership does not prove that an underlying process stopped; inspect it before replacement.

## 5. Checkpoint minimum

Record the mandate and package; worktree, branch, base and head SHAs; dirty-tree status and an exact preserved patch reference; ownership mode and claim/fence; commands, exit codes, outputs, environment tuple and live process/session handles; acceptance and independent-verification state; evidence references/digests; decisions and failed hypotheses; blockers; and the next concrete command or action with its expected result.

A narrative saying “almost done, run tests” is insufficient. A screenshot is not a substitute for commands and state. Do not retain raw credentials, secret-bearing environment dumps or complete model conversations by default. Preserve authorized references and redacted diagnostics.

## 6. Resume procedure

1. Verify the recorded worktree, base/head and diff. If absent, reconstruct the exact revision and patch into a fresh isolated worktree.
2. Inspect outstanding processes and external effects. Reconcile unknown outcomes before retrying non-idempotent actions.
3. Obtain a fresh claim or coordinator assignment. A checkpoint does not renew expired authority.
4. Revalidate changed assumptions: dependency commits, tool availability, expiring grants, running providers and contract revisions.
5. Execute the recorded next action; revise the checkpoint when new evidence changes the plan.

## 7. Independent qualification

The author submits a reproducible recipe. A different agent/person executes package-critical positive and forbidden paths on the submitted revision and inspects whether fixtures match the claim. The verifier may use the same model family; independence means separate execution and judgment, not a formal assurance claim. Extra specialist review belongs to a declared release profile.

No available verifier means `implemented`, not `qualified`. Continue independent work while retaining the outstanding verification. Qualification is not a queue on every commit. After a revision, assess impact and rerun affected checks; do not carry evidence across materially changed code, schemas, policy or providers without justification.

## 8. Blockers and bounded investigation

A blocker records type (`authority`, `access`, `resource`, `contract`, `dependency`, `defect`), affected acceptance IDs, evidence, attempted remedies, smallest resolving decision and independent work still possible. Missing an optional adapter blocks that adapter, not local operation. Missing required containment blocks every profile claiming it.

Investigate with a question, experiment and decision threshold. Repeated retries without new evidence trigger a different method or a bounded spike. Escalation is concrete: the prepared change, observed gap and decision needed. Do not turn an implementation choice or unavailable optional repository into a request for blanket permission.

## 9. Exit conditions

Stop when the assigned scope is qualified, the mandate expires, the user interrupts, resources are exhausted or every remaining authorized path is concretely blocked. Technical session limits require a checkpoint. Completion reports state the achieved claim, pending qualification and deferred profiles; they never equate session end with roadmap completion.
