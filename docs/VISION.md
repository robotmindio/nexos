# NexOS vision

**Status:** proposed product direction. This specification does not assert that NexOS has been implemented or that the product hypotheses have been validated.

## 1. The product promise

NexOS is an operating environment in which a person can create a persistent workspace, give it a bounded objective, work directly alongside agents, and inspect or recover the resulting changes. The workspace retains the identity of the work when a window closes, a model changes, or a worker restarts.

The intended experience is concrete: open a project, see the current artifacts and unfinished work, delegate a change, continue editing, compare the result against the original, and retain exactly the outcome you intended. The same environment can later coordinate research, business operations, and physical devices through separately qualified capabilities.

The central product hypothesis is that **preserving the relationship between intent, authority, state and evidence reduces the manual coordination required to complete real work**. This is a hypothesis to test against ordinary Linux tools and existing agent workflows. A larger feature count, more autonomous steps, or a convincing conversation does not establish it.

“OS” describes the long-term scope. The initial implementation is a portable Linux runtime and workspace shell with a controlled reference environment. A NixOS distribution is a later integration and delivery surface. Useful product behavior must arrive before the project takes responsibility for an entire daily-driver distribution.

## 2. What is new at the system boundary

Applications remain useful. NexOS adds an operating contract across applications and agents: a work item has durable identity, a provider advertises an operation, a principal holds limited authority to invoke it, and an effect produces a receipt. The shell presents these relationships consistently.

| User concern | NexOS product requirement |
|---|---|
| “What are we trying to do?” | An editable objective, constraints and acceptance evidence survive conversations. |
| “What can it touch?” | The workspace shows managed resources and effective permissions before delegation. |
| “What is happening?” | A task presents current execution state, meaningful outputs, blockers and cost. |
| “Can I take over?” | Direct tools and agents operate the same typed capabilities; edits use revisions and conflicts. |
| “Can I try another approach?” | Managed branches isolate supported state and expose their coverage. |
| “What actually changed?” | Promotion presents resource-level differences and effect outcomes. |
| “Can I trust this result?” | Evidence identifies observations, sources and verification limits separately from interpretations. |
| “Can I leave and return?” | Durable work resumes according to its declared execution profile. |

A workspace is not automatically a sandbox, transaction, distributed filesystem, or synchronized copy of every application. These are distinct services with declared coverage. The product must make that coverage legible.

## 3. The first customer and first complete experience

Start with a technically capable individual working on a software or research project on Linux. This concentrates the initial problem around artifacts, reproducible tools, expensive context switching and recoverable changes. It is narrow enough to qualify without first implementing arbitrary enterprise workflows or robotic safety.

The initial complete experience is a **managed project workspace**:

1. Select a project and explicitly enroll its managed resources.
2. Open conventional editors and a terminal alongside a stable work board.
3. Create an isolated branch for a bounded change or experiment.
4. Run deterministic tasks, then a real bounded agent when the AI profile is qualified.
5. Inspect diffs, outputs, evidence and unresolved effects.
6. Promote supported changes, resume interrupted work, or discard the branch.

The runtime must provide useful manual operation first. A shell that only displays counters while requiring every meaningful operation through conversation fails this product direction. Equally, a deterministic task manager alone does not demonstrate the AI-native claim: an adaptive agent must use structured context, react to observations, and complete qualified tasks under the same controls.

## 4. AI-native means shared system services

AI capability is native when agents consume system-maintained context, invoke discoverable capabilities, keep durable plans and executions, use explicit authority, and expose meaningful correction points. The model does not have to reconstruct the entire computer from screenshots or own the only copy of task state.

The architecture is deliberately asymmetric: planning and interpretation can be probabilistic; authority, state transitions and effect admission are enforced independently. An agent may propose a new tool, procedure or view. That proposal becomes usable only after the relevant validation and permission steps. Self-modification must not alter the agent's own acceptance criteria or grant it broader authority.

Model-free operation is an availability requirement for the substrate, not a claim that model-dependent work can continue without inference. When inference is disabled, workspaces, typed operations, saved procedures, evidence and recovery remain usable. New natural-language interpretation or adaptive planning may become unavailable, with that condition shown explicitly.

The detailed AI service contract and evaluation design live in [AI-NATIVE.md](AI-NATIVE.md).

## 5. Benefits that do not depend on AI

NexOS should remain valuable when every model provider is disconnected. The first benefits are recoverable changes, persistent workspaces, explicit delegation, inspectable history, interoperable operations and portable artifacts. A deterministic program should be able to use all of them.

This creates several longer-term possibilities:

- **Personal computing with continuity:** restore work context and supported task state without forcing all data into a cloud account.
- **Software by composition:** combine independently developed operations and views while preserving each provider's ownership and security contract.
- **Reproducible investigation:** retain data versions, procedures, observations and unresolved claims instead of only a final report.
- **Controlled organizational delegation:** grant a service or colleague a task-specific envelope rather than share a user's entire account.
- **Federated computing:** move supported work between authorized resources while retaining identity, budget and history.
- **Assistive interaction:** offer equivalent keyboard, visual, command and conversational surfaces over the same operations.

These are product directions, not automatic consequences of using Linux, Nix, a graph database, or an LLM. Each requires an independently demonstrated experience.

## 6. Scope boundaries that protect the vision

NexOS preserves conventional Linux applications; it does not initially replace POSIX, the compositor, the kernel or general-purpose databases. It does not promise universal undo, global atomic changes, transparent migration of arbitrary processes, complete observation of all computer activity, or proof that model conclusions are true.

The early product does not require a capability marketplace, a new programming language, a new vector database, multiple inference gateways, active-active federation, GPU scheduling, a consumer app ecosystem, or physical actuators. These may become justified extensions. They must not become prerequisites for opening a workspace and doing useful work.

Reuse in RobotMind is selective and evidence-based. Existing projects are candidates for durable execution, knowledge, identity and interaction. NexOS should contribute the common operating contract and product integration without recreating them or importing every dependency into the local boot path.

## 7. What would falsify the approach

The direction needs revision if users repeatedly leave NexOS to understand its own state; if manual work becomes slower because of unnecessary ceremony; if narrow grants cannot be enforced; if every integration needs bespoke orchestration; or if the agent's apparent success depends on relaxed verification.

The initial evidence should answer three questions: does the workspace reduce coordination, does recovery preserve useful work under real failures, and does structured system access improve agent outcomes at a controlled cost? [PRODUCT-DESIGN.md](PRODUCT-DESIGN.md) defines the observable behavior; [USER-EXPERIENCE.md](USER-EXPERIENCE.md) gives complete journeys; [OPPORTUNITY-COSTS.md](OPPORTUNITY-COSTS.md) defines decision gates for expanding the scope.
