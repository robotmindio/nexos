# User journeys and visible outcomes

**Status:** product specification. The E01–E10 identifiers connect these journeys to conformance scenarios. Product descriptions do not count as executed acceptance evidence.

## 1. The common workspace

Every journey begins in the same recognizable environment: an open project, its work board, artifacts, active branch and activity. The user can inspect scope, work directly, or delegate. The shell shows the current execution location and whether that state is live or last known.

| Area | Example contents before work | Contents after useful work |
|---|---|---|
| Work board | “Update the analysis”; acceptance criteria; available inputs | Outcome, checks, unresolved decisions and next action |
| Artifacts | Source tables, report, scripts, data revisions | New report revision, figures, executable procedure |
| Branch panel | Baseline; managed files; excluded resources | Selectable differences, conflicts and recovery coverage |
| Activity | Recent human edits and completed operations | Observed effects, sources and verification results |
| Authority | Allowed reads/writes; no network; remaining budget | Actual usage; current grants; any expansion request |

These are illustrative contents, not demo data to display when production data is missing.

## [E01](../conformance/experiences/E01.md) — Try a change and keep the result

**Before.** Open a project with a working baseline. Select “Create branch.” The scope preview includes project files and a supported environment definition; unrelated home files and remote services remain excluded.

**During.** In the branch, install a declared project dependency, edit a service or analysis script and run real validation. Use the editor manually or delegate exactly the same operations. The task panel links failures to logs and affected resources. Normal work in the baseline can continue under the supported isolation profile.

**After.** The comparison presents source differences, environment changes, generated artifacts and checks. Select supported changes for promotion. A changed baseline produces a conflict instead of overwriting newer work. Unsupported merge types offer a whole-resource choice or explicit manual resolution.

**Failure path.** Interrupt promotion between provider steps. On reopening, the task identifies completed, pending and unknown outcomes and offers the provider's supported recovery actions. It never says “everything rolled back” solely because the branch pointer was restored.

**Value.** Experiment freely while seeing the actual boundary of isolation and recovery.

## [E02](../conformance/experiences/E02.md) — Leave, restart and resume

**Before.** Start a durable task with a visible execution location and checkpoint policy. If it runs only on the laptop, closing the application differs from powering off the machine.

**During.** Disconnect the client or restart a worker. The task retains identity and committed outcomes. If the execution host goes offline, the UI shows that work has paused or its status is unknown; it does not promise that powered-off hardware keeps computing.

**After.** Reopen on the same client, or on a second authorized client connected to the execution service. Resume from validated state. The task shows what was completed, what is being retried, and what needs reconciliation.

**Failure path.** A remote provider accepted a non-idempotent request before the response was lost. Show “outcome unknown,” with reconciliation instructions. Do not repeat it merely to make the progress bar advance.

**Value.** Continuity follows the execution profile and surviving host. Device-loss survival additionally requires the qualified backup or remote-execution profile.

## [E03](../conformance/experiences/E03.md) — Create a tool for the problem at hand

**Before.** A workspace has qualified operations for listing experiments, reading results and starting an allowed run. Ask for a comparison view, or compose it manually from those capabilities.

**During.** Preview a table and parameter form over authorized data. A later renderer profile may add charts. Inspect metric definitions, units, source bindings and permitted actions. The generator proposes a layout; the trusted renderer and broker constrain behavior.

**After.** Save the view. Reopen it without the model, edit a column directly, and invoke a permitted operation. Export the view declaration and dependency references.

**Failure path.** A missing provider produces a visible unavailable control. A schema mismatch produces a repair action. A generated button cannot obtain broader authority by claiming that an action is safe.

**Value.** Create durable, task-specific interfaces without making every user a front-end developer. The first implementation supports a bounded component vocabulary.

## [E04](../conformance/experiences/E04.md) — Delegate without surrendering the workspace

**Before.** Give two agents different subtasks: one reads selected sources and proposes edits; another executes permitted validation in a branch. Their effective grants are inspectable.

**During.** The agents share approved artifacts and receipts. A forbidden file, destination or budget increase is denied at the enforcement boundary, even if requested in valid tool syntax. Existing authorized work proceeds without repeated prompts.

**After.** Inspect each principal's changes and usage. Revoke one grant while keeping the other task active. The UI shows acknowledgement boundaries and any already-dispatched effect that may still finish.

**Failure path.** A child asks for parent credentials or attempts to bypass the broker. Qualification requires prevention under the declared isolation profile, not merely a polite model refusal.

**Value.** Delegate meaningful responsibility with a comprehensible limit on what can happen.

## [E05](../conformance/experiences/E05.md) — Understand where an artifact came from

**Before.** Select a result that looks wrong. Open “History and evidence.”

**During.** Traverse the producing execution, input revisions, operations, actor and verification outcomes. Expand only authorized payloads. Ask for an explanation if desired, with links to the observed records.

**After.** Identify an outdated input or failed assumption and create a corrective task. The explanation is labeled as interpretation; the causal records remain available independently.

**Failure path.** A source was not captured, is now inaccessible, or was deleted under retention policy. Show that gap explicitly. An agent cannot fill it with an invented causal story.

**Value.** Investigate actual work without reconstructing it from chat or treating every event timestamp as proof of causation.

## [E06](../conformance/experiences/E06.md) — Turn a demonstrated procedure into a reusable capability

**Before.** Enable semantic action capture for a selected task. The capture scope and stop control are visible.

**During.** Perform a routine transformation across supported operations. The system proposes parameters, conditions and output checks. Review which details are constants and which vary. Confirm that credentials and private input were excluded.

**After.** Validate on different authorized inputs in isolation, save a versioned procedure, and run it without inference. Inspect its dependencies, effect envelope and failure behavior.

**Failure path.** A step was an opaque click sequence or depended on an unrecorded human judgment. Keep it as a manual checkpoint or unsupported step; do not market it as a generalized semantic operation.

**Value.** Reuse an operation learned from work while retaining an inspectable program and a clear validity domain.

## [E07](../conformance/experiences/E07.md) — Use another machine's resources

**Before.** A second authenticated node offers a supported execution resource. The workspace authority decides whether the task may use it and which data may leave the local node.

**During.** Start an eligible task remotely. Show locality, transfer progress, cost and lease. Closing the local UI does not cancel the remote worker unless requested.

**After.** Receive typed outcomes and artifacts; retain their remote provenance. Continue local work against a fresh revision.

**Failure path.** Partition the network or expire the lease. The interface shows last-known state and fences stale commitments where the provider supports fencing. A task cannot be safely resumed elsewhere until the old executor's authority and ambiguous effects are resolved.

**Value.** Compose resources without promising unrestricted process migration or conflict-free active-active workspaces. Robots require an additional safety profile and are outside this initial experience.

## [E08](../conformance/experiences/E08.md) — Use the computer without a model

**Before.** Disconnect inference. Open the workspace in the qualified Linux environment or reference image.

**During.** Use an ordinary editor, terminal and application. Run registered deterministic operations, inspect grants, create a branch, invoke a saved procedure and consult history through direct controls.

**After.** Save, close and resume supported work. Export artifacts in documented formats. No model is needed to recover an admitted deterministic task.

**Failure path.** Natural-language planning or a model-dependent operation is unavailable. Its control says why and offers direct alternatives when they exist. The system does not silently transmit data to a remote provider.

**Value.** The platform remains a useful computer and a reliable substrate when inference is unavailable, expensive or unwanted.

## [E09](../conformance/experiences/E09.md) — Complete an adaptive task under bounded control

**Before.** Choose a real task with outcome checks, such as updating a report after a source schema change or fixing a failing project test. Set the allowed resources, operations, time and inference budget.

**During.** A real agent discovers relevant capabilities, reads structured context and selects actions. A failed precondition requires a revised plan. The user edits an artifact midway; resumption observes the new revision instead of overwriting it.

**After.** The agent presents outputs, concise decisions and acceptance evidence. A separate validator or review role checks the declared outcome. The user can inspect and promote the result without trusting the agent's confidence alone.

**Failure path.** A source contains hostile instructions or the budget runs out. Authority remains unchanged, costs are accounted for, and the task stops or requests a specific authorized adjustment.

**Value.** Demonstrate adaptive intelligence using native services. This experience cannot be qualified by replaying a scripted conversation.

## [E10](../conformance/experiences/E10.md) — Upgrade and recover the environment

**Before.** Inspect an available runtime or image update, its schema compatibility and recovery plan. The preview identifies restart requirements and data migrations.

**During.** Apply the update under the appropriate maintenance profile. Existing tasks checkpoint or stop at defined boundaries. A migration has its own recovery coverage; selecting an earlier system generation is not presented as restoring arbitrary data.

**After.** Reopen workspaces and inspect task continuity. Validate a restoration from an actual backup into a separate environment; snapshot existence alone is insufficient.

**Failure path.** The update cannot reopen the previous metadata format. Show the compatible backup or migration recovery path and preserve evidence of partial changes. Never overwrite the last recoverable state to make a rollback look clean.

**Value.** A durable operating environment must survive its own evolution. Distribution qualification adds installation, boot and hardware-specific requirements beyond the portable runtime.

## 2. Cross-journey acceptance

Every qualified journey needs a positive path, an interruption or fault path, a direct-control path, and accurate presentation of limits. CLI and GUI must resolve to the same state and authority. Journey requirements are translated into executable cases in the conformance program; no screenshot, conversation or narrative establishes completion by itself.
