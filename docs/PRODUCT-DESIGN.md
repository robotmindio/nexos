# Product design and interaction contract

**Status:** requirements for product surfaces as they are introduced. The engineering program determines which surface is qualified in a release. Illustrative labels below are proposed UI text, not screenshots of an implementation.

## 1. Stable workspace shell

The first graphical surface is a normal application on the existing desktop. It must not require a new compositor. A persistent workspace is the main navigational unit, with recognizable projects and artifacts rather than an inbox of unrelated conversations.

| Surface | Default contents | Primary actions |
|---|---|---|
| Workspace switcher | Recent projects, unresolved work, device availability | Open, create, archive, export |
| Work board | Objectives, active tasks, waiting decisions, saved procedures | Create task, resume, pause dispatch, inspect |
| Artifact view | Files and typed artifacts, revisions, managed scope | Open in application, compare, branch |
| Activity view | Significant actions, outcomes, causal links | Inspect evidence, filter, export |
| Authority panel | Effective grants, destinations, limits and expiration | Narrow, revoke, extend within user authority |
| Resource panel | Compute, storage, inference and spending state | Adjust authorized budget, stop admission |
| Command palette | Authorized entities, operations and optional interpretation | Navigate, preview, invoke |

Core navigation, authority controls and recovery actions have fixed locations. Generated content may occupy a workspace view; it cannot impersonate shell controls, replace trusted permission UI, or silently rearrange the user's desktop. Optional chat belongs inside work, with its messages linked to tasks and artifacts.

A task remains the same object when the user switches from chat to a table, terminal or editor. A conversation is one interaction record, not the durable definition of the task.

## 2. Enrolling a project

On first use, the user selects a directory or resource collection. The preview lists what NexOS will manage, what it will only read, and what remains outside its scope. The first operation must not recursively capture the whole home directory or import credentials.

Enrollment supports a copied or isolated managed workspace as the default for experimentation. Direct management of existing data requires an explicit description of the recovery mechanism. Imported data keeps its provenance and source relationship; importing a copy does not grant authority over the original.

Before the first task, the user can see available local capabilities and whether a model provider is connected. The interface must remain useful without either an external account or a model. Optional integrations are added as needed and their unavailable state does not prevent local manual work.

Legacy applications open normally. A visible integration status distinguishes a managed artifact, an application with qualified semantic operations, and an ordinary application whose unsaved state NexOS cannot recover. A window appearing inside a workspace is not evidence that all of its activity is mediated.

## 3. The delegation surface

An objective is translated into an editable work request containing outcome, input scope, permitted operations, budget, deadline and required evidence. Ambiguous instructions may need interpretation, but existing explicit grants and previously chosen constraints should be reused.

For a bounded task, the user sees a compact summary such as:

> Update the report using these three datasets. Work in a branch. Read these inputs; write this report and its figures. No external requests. Stop after the time budget. Keep the source data unchanged.

The detailed view resolves that summary to exact resources, capability versions and limits. Permission expansion is a separate operation from approving the quality of a result. A model cannot relabel a wider permission request as a harmless retry.

Actions within an already authorized envelope should proceed without repetitive confirmations. New destinations, broader data access, increased spending, publication and other envelope changes produce a concrete decision card. The system groups related decisions when doing so preserves their meaning. It does not ask for a generic “trust agent” toggle.

The approval surface identifies the actual effect, destination, initiating principal, applicable grant and remaining uncertainty. A preview may be an estimate; it must not be presented as guaranteed execution output. If no reliable preview exists, say what is known rather than inventing a diff.

## 4. Direct manipulation and agent handover

The user can inspect and edit plans, artifacts and configuration using familiar controls. When an agent and a person edit the same managed resource, revisions and conflicts are explicit. Neither actor silently wins because it is “more intelligent” or arrived last.

“Take over” requests a pause of new agent dispatch for the relevant task and shows any running effects. The UI confirms the pause only after the relevant boundary acknowledges it. A resource still being written is not presented as exclusively handed over; the user waits for a safe boundary or edits a separate branch with supported conflict handling. The user may leave a concise instruction for subsequent resumption. The task retains its history and authority; taking over is not equivalent to revocation unless the user selects that action.

Manual changes outside managed interfaces are detected when the relevant adapter can detect them. They invalidate stale previews or claims of unchanged state. If an adapter cannot detect a class of change reliably, its UI must expose that limitation and require fresh validation before promotion.

“Resume with agent” hydrates a fresh authorized context from the current revision. It must not reuse an old conversation summary as if manual changes had not happened.

## 5. State and failure presentation

The UI derives state from canonical task and effect records. Color or an agent's explanation cannot override those records. Useful labels include:

| Observed condition | User-facing meaning | Available next step |
|---|---|---|
| Waiting for input | A specific value or decision is missing | Supply it, narrow scope, cancel |
| Waiting for resource | Work is admitted but required capacity is unavailable | Wait, choose another permitted resource |
| Running | An execution is active; progress is observable | Inspect, pause new work, request cancellation |
| Pause requested | New dispatch is stopped; existing effects may finish | Inspect running operations |
| Disconnected | This client cannot establish current remote state | Reconnect; inspect last-known timestamp |
| Partially completed | Some outcomes exist; the objective is incomplete | Keep outcomes, retry eligible steps, compensate |
| Stopped; effects unresolved | New dispatch is stopped; the task remains reconciling until linked effects are resolved | Inspect and reconcile those effects |
| Outcome unknown | An effect may have happened but lacks a trustworthy result | Reconcile; do not blindly repeat |
| Conflict | The target changed since the preview or plan | Compare, merge where supported, replan |
| Verified complete | Defined acceptance checks passed for the stated scope | Inspect evidence, promote or archive |

Show last-known state and freshness when disconnected. A spinning indicator must not imply that a remote worker is still alive. Separate “stop asking the model,” “stop new work,” “cancel active execution,” “revoke authority,” and “restore supported state.” The UI can offer a safe combined stop action, but its receipt must explain what actually stopped.

Recovery presents concrete alternatives with consequences. Unknown outcomes cannot be converted into success by dismissing a notification. A compensated external action remains in history; it is not erased as though it never happened.

## 6. Branches and promotion

The branch view lists the baseline revision, included resources, isolation profile, unsaved or unmanaged data, and external effects that cannot be undone. Users can compare outputs without understanding the underlying snapshot technology.

Promotion is a reviewable operation. The UI groups differences by resource and shows conflicts, preconditions, service restart requirements, validation evidence and recovery coverage. “Promote selected changes” is available only for resource types whose providers support that granularity. Unsupported resources are promoted as whole units or remain unselected; the UI must not fabricate a universal three-way merge.

Cross-resource promotion may complete partially. Present each provider's state and an overall result. A single success animation must not hide an unresolved database migration or external write. A workspace label or generation pointer does not itself prove that every external resource changed atomically.

## 7. Generated and reusable views

A generated view is a versioned declaration over allowed components, queries and capability references. The trusted renderer enforces component limits and bindings. It does not execute model-provided privileged JavaScript or accept instructions that imitate the permission surface.

Before saving, the preview distinguishes live data, sample data and missing sources. Production screens must not silently substitute examples for failed queries. Display units, definitions, freshness and source links for consequential figures. A semantic type mismatch, such as mixing durations and monetary amounts, is rejected or surfaced rather than formatted away.

The user can edit layout and bindings directly, revert a view version, inspect its dependencies, and export it without the original model. Changing a capability version may invalidate a view; the shell presents a repair flow instead of executing a different operation under the same button label. Changing display text cannot broaden authority.

## 8. Privacy, accessibility and attention

Recording is selective. Semantic action capture needs a visible scope and stop control; it does not imply keylogging, continuous screenshots, clipboard capture or capture of password fields. Workspace history shows relevant operational facts without storing private model reasoning. Export previews include sensitive payload and attachment choices.

For web-rendered surfaces, adopt WCAG 2.2 AA as the accessibility target and report the actual audited coverage. This target includes keyboard operation, identifiable controls, visible focus, status announcements and understandable errors; it is not a claim that NexOS is currently conformant. Native integration also needs assistive-technology testing on the qualified desktop. [Source: W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

An operation available through drag-and-drop must have a keyboard equivalent. Agent updates should not steal focus. Significant state changes are announced without reading every log line. Motion is optional, color is supplementary, and time-sensitive grants must show understandable expiration. Notification volume is controlled per workspace, with urgent unresolved effects distinguishable from routine completion.

## 9. Product evaluation

Before expanding scope, run paired task studies on the qualified environment. Include ordinary manual operation, interrupted work and adaptive agent tasks. Compare conventional tools, NexOS without a model, and NexOS with a model where applicable. Record setup costs separately so a reusable workspace does not hide expensive onboarding.

Measure successful completion, time actively spent coordinating, number of interventions, time to resume after interruption, error recovery, unwanted effects, and participant understanding of scope. Measure resource consumption and model cost separately. Report per-task results and failure cases; a small exploratory sample does not justify population-level claims.

The first study should include at least three task families and both experienced and unfamiliar operators where practical. Freeze the task set and success predicates before implementation-specific tuning. A release gate requires all safety and recovery checks for its profile plus evidence that the main user experience is usable; performance targets are recorded before the qualifying run. A good demo does not substitute for these observations.
