# AI-native services and qualification

**Status:** proposed contracts for an adaptive-agent profile. No model integration, agent benchmark or AI capability is qualified by the existence of this document.

## 1. The claim to demonstrate

An AI-native NexOS must do more than execute a predetermined workflow. In E09, a real model must inspect authorized structured state, choose a course of action, use real capabilities, respond to new observations, and produce evidence for a bounded objective. The task's identity, authority, budget and outputs must survive model replacement or interruption.

The deterministic substrate and adaptive agent are separately qualified. The core workspace remains usable without inference. A product claiming the adaptive profile must use actual inference during its qualifying run; recorded completions and scripted conditionals may test components but cannot stand in for that demonstration.

Native services should solve shared problems once: context acquisition, capability discovery, authorization, durable execution, artifact identity, budget accounting and recovery. The agent supplies interpretation and planning. An independent controller mediates every consequential action.

## 2. Structured context is an authorized snapshot

A context service assembles a task-specific snapshot, not an unrestricted copy of the user's computer. The snapshot includes the objective and its revision, permitted resources, relevant artifact revisions, capability contracts, recent effect receipts, outstanding conflicts, remaining budget and time, and references to approved memory.

Each item has a source, access scope, freshness, provenance and sensitivity classification. Context may contain quoted hostile instructions; origin labels and separation from trusted task instructions are required, but do not establish immunity to prompt injection. The broker must enforce authority even when a model follows the hostile text.

Acquisition follows an explicit pipeline:

1. Resolve the authenticated task principal and active grant.
2. Select authorized sources and a bounded retrieval query.
3. Fetch records at declared revisions or label their freshness limits.
4. Apply field and payload policies before transmission.
5. Allocate the context budget while preserving critical constraints.
6. Record the source manifest and produce a model request.

Omitted, unavailable and redacted information must be distinguishable. If a critical precondition is omitted to fit a token budget, the invocation is not admitted until that precondition is checked independently. Summaries are derived artifacts; they cannot silently replace authoritative records or expand permission.

Revocation affects subsequent context reads as well as actions. Cached content is partitioned by authorization and privacy boundaries. An old embedding, summary, prompt cache or agent checkpoint must not provide a backdoor to a revoked resource. Deletion and retention procedures cover derived data; already transmitted content may not be retractable from an external provider.

## 3. Capability contracts need operational meaning

Input/output schemas are necessary but insufficient. Discovery must also expose the resource scope, semantic preconditions, expected outputs, relevant effect dimensions, failure and retry semantics, cancellation behavior and evidence produced. A valid JSON invocation can still be a wrong or unauthorized action.

An adapter might advertise “write report artifact” with an expected revision and content type. It must not advertise a generic shell command as equivalently constrained merely because its input has a JSON string field. Unrestricted shell, UI automation and opaque external tools require a broader declared effect envelope and the corresponding isolation profile.

Preconditions are checked at invocation and, where required, at the effect boundary. A model may suggest a precondition, but provider and policy checks decide whether it holds. Consequential numerical or scientific claims need domain-specific validators; a capability receipt proves an operation's observed outcome, not the truth of every interpretation of that outcome.

## 4. Plan, admit, execute, observe

The agent maintains a versioned plan with proposed steps, dependencies, expected evidence and unresolved questions. The interpreter converts a selected step into a typed request. The broker validates schema, current authority, resource revision, budget and provider readiness before dispatch.

The model never chooses its effective principal by writing a field. Trust comes from the authenticated session and bound execution identity. Likewise, a model-authored “approved” flag has no effect.

The plan is editable by a person and can evolve within its mandate. Scope expansion requires an actual grant update; repeated replanning cannot manufacture more budget. Plan changes, material assumptions and observed outcomes are recorded as concise summaries with evidence links. There is no requirement to retain private model reasoning or a full internal chain of thought.

Workers return observations through typed results. Untrusted tool output remains data when reintroduced to the planner. A successful tool call is not synonymous with an achieved objective. The acceptance evaluator checks the declared result against evidence after the relevant steps complete.

## 5. Durable cognition without storing an illusion of a mind

Persist the objective, plan revision, completed step receipts, relevant artifacts, granted constraints and a reconstructable context manifest. Do not make continuation depend on an opaque provider conversation identifier or an unlimited transcript.

On restart, reconcile effect outcomes first, then hydrate current state. Do not resume from a stale plan while ignoring a manual edit, revoked grant or exhausted budget. Unknown external outcomes block affected retries until reconciliation; the planner cannot turn uncertainty into a safe retry merely by expressing confidence.

A model may change between attempts, but a new model must still satisfy the same capability and policy contracts. The system should expose the change when it materially affects cost, privacy, output quality or the user's constraints. Reusing the same model identifier is not sufficient for reproducibility; record available provider version metadata and request configuration. Exact token-level replay is not a product guarantee.

## 6. Memory and learning

Memory separates confirmed preferences, observed project facts, procedures, inferred hypotheses and transient working summaries. Each class has an owner, provenance, revision, access policy, retention rule and a way to correct or retire it. Retrieval ranking is an aid to selection, not an authority or truth metric.

A successful sequence may become a proposed procedure after parameters, preconditions, side effects and recovery behavior are made explicit. Demonstration capture alone does not establish that the sequence generalizes. The user can inspect and edit the procedure, and qualification uses cases that differ from the demonstration.

Tool or runtime improvement is a normal change proposal: branch, implement, validate, compare and authorize promotion. An agent may not modify its acceptance oracle, security policy or evidence records to declare its own improvement successful. Learning new affordances never automatically grants authority to use them.

## 7. Inference as a resource

Use the existing qualified inference gateway when available; add a thin NexOS adapter rather than a second gateway. A local inference provider is optional and independently qualified. GPU scheduling is a later resource profile, not a prerequisite for local deterministic work.

A request records provider and model selection, approved payload classification, timeout, maximum output, cost policy, cancellation semantics and task association. Automatic failover is permitted only to providers that satisfy the same privacy and authority constraints. Failing from a local-only request to a remote service is not a harmless implementation detail.

Separate measured usage, reserved limits and estimated bills. External inference may have an uncertain final charge; the product must expose the enforceable bound or uncertainty rather than imply perfect control. Repeated inference attempts consume the same task budget. Remote inference also counts as data egress even when it produces no local file mutation.

## 8. Multi-agent work and human intervention

Subagents receive narrower mandates and independently authenticated execution identities. They share task references and authorized artifacts, not unrestricted copies of the parent's context or credentials. Parent and child reservations must not double-spend the same budget.

Parallel exploration belongs in isolated branches. Merge results through typed resources and fresh validation; “the subagent said it passed” is an assertion until evidence is checked. A cancellation or revocation propagates according to its defined enforcement boundary, with in-flight outcomes still visible.

Human intervention can correct the objective, edit artifacts, narrow authority or stop dispatch. Resumption rechecks all changed constraints. The useful product property is continuity of work and control, not persistence of a particular conversational persona.

## 9. Evaluation and release evidence

Freeze evaluation tasks and acceptance predicates before optimizing the agent. Include unfamiliar inputs and interruptions, not only rehearsed demonstrations. The initial adaptive suite should cover a bounded project change, a multi-artifact analysis task, and a task that requires revising a plan after a failed precondition. Use actual projects or qualified realistic datasets; do not disguise synthetic data as external evidence.

Compare manual operation, deterministic composition where possible, and adaptive execution with the same permissions and resource limits. A useful ablation compares structured NexOS context against the same agent with reduced structured context. Report task completion, correctness, unauthorized attempts versus prevented effects, operator corrections, latency, inference usage and recovery outcomes.

Adversarial cases include hostile source instructions, stale state, malicious capability descriptions, forbidden destinations, credential requests, invalid tool arguments, budget exhaustion and revoked access. Passing a finite suite is evidence for that suite, not a general prompt-injection defense.

The qualification report identifies task set, model/provider configuration, code and schema revisions, environment, budgets, source manifests, outputs, validators and failure cases. Security invariants have no trade-off against average success rate. Another model can be evaluated later without redefining the operating contract; performance claims apply only to tested configurations.
