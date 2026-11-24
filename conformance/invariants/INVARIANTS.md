# Required invariants

Status: runtime implementation and qualification pending. These are normative properties with falsification procedures, not assertions that the properties currently hold. Canonical coverage is [matrix.json](../matrix.json). I20 governs engineering evidence; other entries describe system behavior within a declared profile.

## I01 — No unauthorized mediated effect

**Rule.** For every effect, the actual enforcement point validates an authenticated principal, current grant, operation, target and policy. A denied request leaves the target unchanged. Direct syscall/network bypass is tested for the claimed containment profile.

**Attempt to falsify.** Issue a forged request, wrong-workspace target and direct bypass from a real untrusted worker; observe denial and target state.

**Normative owner:** [docs/SECURITY.md](../../docs/SECURITY.md).

## I02 — Delegation cannot amplify authority

**Rule.** A descendant grant can only narrow operation/target scope, validity, delegation depth and enforceable budget. A child cannot convert estimated cost into an unlimited parent liability.

**Attempt to falsify.** Construct child grants exceeding one parent dimension at a time and race simultaneous child budget reservations.

**Normative owner:** [docs/SECURITY.md](../../docs/SECURITY.md).

## I03 — Revocation has explicit dispatch semantics

**Rule.** After enforcement acknowledgement, no new admission or dispatch is authorized at the controlled enforcement point under the revoked authority. Already-dispatched work retains its declared completion/reconciliation semantics. Revocation is not retrospective undo.

**Attempt to falsify.** Race a stream of operations against revocation and identify the serialized boundary; preserve in-flight effects as visible outcomes.

**Normative owner:** [docs/SECURITY.md](../../docs/SECURITY.md).

## I04 — Retries preserve effect identity and uncertainty

**Rule.** Retry uses provider-supported idempotency and a stable input identity. A changed payload cannot reuse a key. Unknown non-idempotent outcomes are reconciled or quarantined, never blindly retried or declared successful.

**Attempt to falsify.** Crash after external dispatch but before receipt persistence, then resume; use both idempotent and non-idempotent real providers in their qualified profiles.

**Normative owner:** [docs/STATE-AND-RECOVERY.md](../../docs/STATE-AND-RECOVERY.md).

## I05 — Promotion binds to validated revisions

**Rule.** Promotion checks expected branch/base/head and relevant dependency revisions, binds its approval to the actual plan and records per-provider progress. CAS of one pointer does not imply a transaction over all resources.

**Attempt to falsify.** Change the base or a dependency after validation; verify conflict and failed stale approval, then interrupt each promotion stage.

**Normative owner:** [docs/STATE-AND-RECOVERY.md](../../docs/STATE-AND-RECOVERY.md).

## I06 — Branch and workload boundaries protect the base

**Rule.** Mutations in a branch or untrusted workload cannot modify protected base/host resources outside its declared capability. Snapshot naming alone is not isolation.

**Attempt to falsify.** Attempt traversal, symlink escape, inherited descriptor abuse and direct writes from a real branch worker.

**Normative owner:** [docs/SECURITY.md](../../docs/SECURITY.md).

## I07 — Durable work resumes from consistent checkpoints

**Rule.** A task outlives its client/process through persisted state with explicit attempt identity, checkpoint compatibility and authority revalidation. Recovery never treats a stale checkpoint as renewed permission.

**Attempt to falsify.** Kill worker/daemon at checkpoint boundaries, revoke authority, restart and verify state plus effect behavior.

**Normative owner:** [docs/STATE-AND-RECOVERY.md](../../docs/STATE-AND-RECOVERY.md).

## I08 — Managed effects have attributable observed evidence

**Rule.** Each mediated committed or unknown effect records actor, authority reference, capability/version, causal context and receipt status. Observed facts, assertions and inferred relationships remain distinguishable.

**Attempt to falsify.** Trace an actual artifact to accessible inputs/receipts, then remove evidence access and verify that missing provenance remains unknown.

**Normative owner:** [docs/ONTOLOGY.md](../../docs/ONTOLOGY.md).

## I09 — Core operations do not require inference

**Rule.** Workspace inspection, authorization, ordinary managed operations, recovery and deterministic saved procedures continue without a model or optional remote service. Inference-dependent operations clearly report unavailability.

**Attempt to falsify.** Disable model access and optional cloud services; complete the declared deterministic CLI/UI experiences.

**Normative owner:** [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md).

## I10 — Expired federated ownership cannot commit fenced work

**Rule.** An expired/superseded lease cannot commit managed work at a resource that enforces its fence. Non-fenceable external effects are identified and never inherit this stronger claim.

**Attempt to falsify.** Partition the current owner, admit a replacement and submit the stale owner’s pending commit at the real enforcement boundary.

**Normative owner:** [docs/STATE-AND-RECOVERY.md](../../docs/STATE-AND-RECOVERY.md).

## I11 — Secrets and nonconsented payloads stay out of context/capture

**Rule.** Secrets use authorized references; default logs, prompts, demonstrations and exports do not contain their values. Capture scope and retention are explicit.

**Attempt to falsify.** Inject uniquely marked secrets and nonconsented events, exercise logging/capture/retrieval/export, and inspect authorized outputs for leakage.

**Normative owner:** [docs/SECURITY.md](../../docs/SECURITY.md).

## I12 — Enforceable reservations cannot oversubscribe limits

**Rule.** Admission and reservation are atomic within the canonical budget owner. Unresolved effects retain liability. Estimated/provider-billed costs are labeled and cannot be sold as hard-enforced ceilings.

**Attempt to falsify.** Race admissions at the limit; crash during settlement; reconcile a delayed provider bill without falsely releasing pending reservations.

**Normative owner:** [docs/PROTOCOLS.md](../../docs/PROTOCOLS.md).

## I13 — Context remains authorized, attributed and freshness-scoped

**Rule.** Context entries carry source, observation/revision, visibility and freshness/uncertainty. Retrieved instructions cannot expand authority. Authorization and relevant state are rechecked before effects.

**Attempt to falsify.** Revoke a context source, change its revision and inject instructions asking for forbidden actions; check actual dispatch and context receipts.

**Normative owner:** [docs/AI-NATIVE.md](../../docs/AI-NATIVE.md).

## I14 — Approval binds to the exact actionable change

**Rule.** Approval refers to an immutable plan/effect summary and targets/revisions. Material plan, target, cost or capability changes invalidate the binding under policy; approval of a goal is not arbitrary effect authority.

**Attempt to falsify.** Change a reviewed target, parameter or capability version before dispatch and require a valid refreshed binding.

**Normative owner:** [docs/PRODUCT-DESIGN.md](../../docs/PRODUCT-DESIGN.md).

## I15 — Updates and restore respect recovery/data compatibility

**Rule.** A claimed update profile provides a tested recovery route and explicit runtime/data compatibility. Configuration rollback does not silently revert or corrupt incompatible mutable data.

**Attempt to falsify.** Interrupt update/restore stages; attempt incompatible downgrade; exercise actual documented recovery.

**Normative owner:** [docs/STATE-AND-RECOVERY.md](../../docs/STATE-AND-RECOVERY.md).

## I16 — Versioned contracts reject incompatibility

**Rule.** Clients/providers negotiate supported contract versions. Missing required semantics, unknown privileged operations and incompatible schemas fail explicitly. Successful parsing is not proof of semantic preconditions.

**Attempt to falsify.** Use unsupported versions, unknown fields where forbidden, invalid bindings and type-correct requests with failed preconditions.

**Normative owner:** [docs/PROTOCOLS.md](../../docs/PROTOCOLS.md).

## I17 — Learned procedures remain bounded and consented

**Rule.** Demonstrations capture consented semantic actions; generated procedures expose parameters, constraints and effects, validate their domain and execute with fresh caller authority.

**Attempt to falsify.** Replay with out-of-domain parameters, revoked authority, changed dependencies and secret-bearing inputs; inspect captured artifacts.

**Normative owner:** [docs/AI-NATIVE.md](../../docs/AI-NATIVE.md).

## I18 — Containment profiles fail closed

**Rule.** A workload cannot claim a sandbox profile when required enforcement facilities, identity separation or egress controls are unavailable. The runtime refuses that profile rather than silently weakening it.

**Attempt to falsify.** Disable a required host facility or remove a needed privilege and attempt profile admission.

**Normative owner:** [docs/SECURITY.md](../../docs/SECURITY.md).

## I19 — Export, deletion and retention preserve current policy

**Rule.** Exports and derived indexes honor current grants and payload-retention rules. Deletion/revocation propagates through defined stores/projections, retaining only permitted audit structure.

**Attempt to falsify.** Delete or revoke a source, query/export from each relevant projection and verify payload access and declared tombstone behavior.

**Normative owner:** [docs/SECURITY.md](../../docs/SECURITY.md).

## I20 — Qualification claims are scope- and evidence-bound

**Rule.** Engineering qualification identifies revision, environment, providers, commands, results and independent reproduction. Specification checks, fixtures and demos cannot establish unexecuted runtime behavior.

**Attempt to falsify.** Submit stale, missing, mock-backed or different-tuple evidence and ensure the qualification process rejects the broader claim.

**Normative owner:** [conformance/ACCEPTANCE.md](../../conformance/ACCEPTANCE.md).

## Interpretation

A passing finite test suite provides evidence within its tuple and threat model, not a mathematical proof covering arbitrary software or adversaries. Where the architecture cannot enforce a proposed guarantee, weaken the claim explicitly through the design process or reject the profile; do not merely soften the test.
