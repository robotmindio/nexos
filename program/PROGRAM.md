# Engineering program

Build a useful managed computing environment before expanding into a reference distribution and federation. Preserve the long-term vision while making each intermediate product claim precise and testable.

[plan.json](plan.json) owns dependency, coverage and qualification-kind references; [state.json](state.json) owns mutable work state. P00 qualifies a specification/inventory deliverable, P14 qualifies engineering procedures, and P01–P13 qualify runtime capabilities. All release profiles require independently verified real runtime evidence; a qualified P00 never implies an operational OS. [EXECUTION.md](EXECUTION.md) defines long-session coordination and continuity. Package IDs represent outcome ownership, not mandatory services, repositories or one-PR-per-package policy.

## Delivery gates

| Gate | Qualified product claim | Excluded from that claim |
|---|---|---|
| M0 | Specification artifacts pass their internal checks. | Runtime or OS behavior. |
| M1 | A useful local managed workspace: bounded operation, branching, durable work, receipts, CLI and human shell. | AI, federation and arbitrary host rollback. |
| M2 | Real adaptive AI work, safe generated views and reusable procedures over the same contracts. | General intelligence or inherent model correctness. |
| M3 | A pinned reference distribution installs, boots, updates and recovers within declared data boundaries. | All hardware and universal data rollback. |
| M4 | Two qualified nodes cooperate through explicit grants, leases and checkpoint transfer. | Transparent arbitrary-process migration or unconstrained active-active writes. |
| M5 | A specific accelerator/toolchain/model tuple executes and accounts for inference. | Other hardware/model combinations. |
| M6 | Named RobotMind adapters meet pinned integration contracts. | Every ecosystem subsystem. |
| M7 | An explicitly selected release profile passes independent integration and lifecycle checks. | Features outside that profile. |

M3–M6 are independent expansion gates subject to actual prerequisites. A runtime release need not wait for robotics, accelerator support or the full roadmap. P14 qualifies individual release profiles as their prerequisites become qualified; every report names its profile.

## Reference implementation

The first runnable qualification target is x86_64 Linux in a QEMU/KVM NixOS VM, CPU only, with managed workspace data and network denied unless a test explicitly needs it. P00 records actual release revisions and toolchain hashes. No release pins, boot results or hardware support are invented in this package.

NixOS is a controlled fixture and later distribution reference. User-space contracts avoid unnecessary Nix coupling; another distribution requires its own qualification. Compilation alone does not establish portability. The reference runtime is a Rust modular `nexosd`, deterministic CLI, isolated workers and narrow privileged helper; SQLite WAL is the initial local canonical metadata store. Internal module/crate choices are ordinary engineering decisions unless they change guarantees.

The bounded local durable-task path has checkpoint and receipt contracts. Audit and integrate Recuriant rather than creating another generic workflow engine. Applicable inference uses the existing Bifrost path when audited and authorized. Local deterministic operations cannot require an optional remote service. [Integration evidence](../docs/INTEGRATION.md) identifies already observed RobotMind surfaces, while their NexOS qualification remains pending.

## Useful parallelism

After P02, branch/promotion work and durable execution can proceed independently. UI implementation may begin against stable contracts while failure qualification continues; M1 requires the integrated result. Distribution and federation are separate expansion tracks. Shared contracts keep one accountable editor; integrations use disjoint worktrees and explicit expected revisions.

Several packages may share a coherent PR. Avoid a queue of fragments that prevents end-to-end qualification. Do not split modules into separate services merely to distribute agent work.

## Discovery and product feedback

P00 audits the smallest dependency set needed for the first vertical path and near-term decisions, not the entire monorepo. Later packages inspect their candidates at pinned revisions. Unavailable access is `unverified`, not evidence that an implementation is unsuitable. Existing session-relay, workspace provisioning, PC control and Bifrost code must be checked before proposing replacements.

Architectural spikes have a question, experiment and decision threshold. Machine-readable contracts and explicit failure semantics are required at component boundaries; formal verification is used for a concrete proof obligation, not as an unbounded precondition to all implementation.

Before optimizing, capture the same user task on conventional Linux and the same hardware tuple. Measure completion rate, interventions, resume time, latency, idle overhead, branch/promotion cost, recovery and model spend. Set numerical budgets after the baseline and before tuning. A dashboard or schema pass cannot replace user-task evidence.

## Release profiles

`local-runtime` requires M1, relevant installation/upgrade checks and P14 integration qualification. `ai-workspace` adds M2 with a named model/provider configuration. `reference-distribution` adds M3 and a pinned image. `federated` adds M4 and the two-node tuple. Accelerator and ecosystem profiles enumerate exactly their M5/M6 additions.

License compatibility and distribution policy are resolved before public redistribution. They do not block authorized local engineering. No profile is currently implemented or qualified.
