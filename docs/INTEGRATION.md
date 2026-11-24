# RobotMind integration and reuse

## 1. What was actually inspected

A bounded read of `robotmindio/robotmind` was performed at commit `d5f2e46d0cb0c73b2c3533415179bbcb887bf33a` on 2026-11-24. The [observation manifest](integration-observations.json) records every full file read and its Git blob identity. Relevant directory listings were also inspected. Two small source modules were read; no builds, services, credentials, hardware or integration tests were exercised.

This is sufficient to identify concrete integration starting points and a few semantic mismatches. It is not sufficient to mark an adapter qualified, prove a documented security property, or certify the whole monorepo. Documentation claims below are explicitly distinguished from runtime evidence. The implementation agent must recheck the pinned sources and their tests before adoption, and record a new revision if it advances the pin.

## 2. Verified discovery and decisions

| Domain | Located evidence | What the inspected material supports | NexOS decision and remaining proof |
| --- | --- | --- | --- |
| Durable orchestration | [`fiber-core/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/fiber-core/README.md), execution lifecycle documentation | Describes Temporal-backed workflows, existing agent execution ownership, durable publication and uncertainty reconciliation. | Adapt Recuriant/Fiber for delegated durable workflows. Prove principal mapping, idempotency, cancellation, recovery and local availability; do not build a second generic orchestration engine. |
| Execution versus recording | [`fiber-core/src/fiber_core/receipts.py`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/fiber-core/src/fiber_core/receipts.py) | Actual code models optional recording-delivery states separately from an action's result. | Do not import recording delivery as proof an effect succeeded. Define separate mappings for execution receipts and epistemic recording observations. |
| Knowledge and provenance | [`knowledge/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/knowledge/README.md) | Documents scoped notes, canonical v0.2 Claims/BeliefStates, artifacts, source hydration and authorization. Old Fact/Belief resource types are documented as retired. | Reuse the current gateway's epistemic contract. Keep NexOS operational state local and authoritative; export permitted observations, not grant truth. Prove retention, offline behavior and current-reader authorization. |
| Inference | [`bifrost/CLAUDE.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/bifrost/CLAUDE.md), [`packages/bifrost-client/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/packages/bifrost-client/README.md) | Describes one gateway codebase with shared/private deployment profiles. The inspected shared client only builds/parses forced-tool calls; transport/retry policy stays with consumers. | Reuse the existing gateway and extend one adapter. Do not create another router. Private/local placement still needs measured egress, model, logging, fallback and cost behavior. Existing profile names do not qualify NexOS. |
| Workspace provisioning | [`packages/workspace-provisioner/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/packages/workspace-provisioner/README.md), `operations.py` | Documents scratch, repository snapshot and repository change workspaces, scoped credentials and existing lifecycle ownership. Explicitly says credential shims are not an OS sandbox. | Reuse the provisioning owner for the existing remote runtimes. Map its work contract to NexOS workspace/branch objects. Add actual local containment without relabeling directory isolation as a security boundary. |
| Agent session continuity | [`agent-session-relay/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/agent-session-relay/README.md) | Describes native hooks, local SQLite spool, connectivity versus activity and uncertain control outcomes. | Reuse session events and proven controls. Do not create a second hook collector. A relay event remains an observation; NexOS task/effect ownership does not transfer to the relay. |
| Desktop control | [`pc/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/pc/README.md) | Documents `/v1/control/*`, local grants, delegated broker proof, compatibility limits and partial Wayland coverage. | Adapt declared capabilities and grants; distinguish structured providers from legacy GUI actions. Do not assume universal Wayland window selection or input control. Exercise each platform path before claiming it. |
| Identity | [`packages/robotmind-auth/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/packages/robotmind-auth/README.md), [`cikut/README.md`](https://github.com/robotmindio/robotmind/blob/d5f2e46d0cb0c73b2c3533415179bbcb887bf33a/cikut/README.md) | Documents shared token verification and Cikut/Keycloak identity. Explicitly separates authentication from each service's authorization. | Reuse the existing authentication boundary through an adapter; map identity to local scoped grants. Do not implement another IdP or require remote SSO to boot or recover locally. |

The source paths retain the name Fiber; Recuriant is the product relationship discussed by the owner. The adapter records exact interfaces and repository paths instead of relying on branding to imply compatibility.

The source inspection also found `packages/knowledge-client`, `packages/noema-sdk` and `app.robotmind.io` paths. Their implementations were not audited here. Secretary, the proposed semantic terminal, the agentic Emacs/IDE and GI remain integration candidates until their precise repositories, revisions and contracts are identified. Failure to inspect them is not evidence that they do not exist.

## 3. State ownership, not duplicate truth

| State | Initial canonical owner | Integration behavior |
| --- | --- | --- |
| Local workspaces, managed resource revisions, grants and reservations | NexOS local runtime | Explicit export; no remote mirror becomes a second authority. |
| Delegated workflow progression | Existing Recuriant/Fiber owner once admitted | NexOS keeps a reference and observed status; never starts a competing retry loop. |
| Local worker supervision and effect reconciliation | NexOS task/execution owner | A small journal for OS operations, not a new generalized workflow service. |
| Epistemic claims and long-term semantic records | Existing Knowledge/NoemaDB gateway | NexOS submits authorized evidence using its current contract. |
| Local artifact bytes and offline metadata | NexOS artifact owner | External copies have explicit IDs, retention, custody and acknowledgements. |
| Model routing/provider credentials | Existing Bifrost deployment/profile | NexOS supplies intent-specific model policy and budget admission; does not duplicate routing. |
| Human identity federation | Cikut/Keycloak via verified adapter | Local enrollment and scoped authority persist independently. |
| Telemetry | OTel exporters and existing backend | Loss or sampling of telemetry cannot remove the authoritative effect journal. |
| Agent native session/control state | Native harness plus existing relay/owner | Observe and invoke supported controls; never infer completion from idle or disconnect. |

An adapter must name which owner retries an operation. Double retries at the client, gateway and durable engine can multiply cost and effects. Enumerate transport retries, model retries and task retries separately; qualify their combination, especially for real tool calls.

## 4. The integration contract

Before enabling an adapter, record:

- Exact repository and revision, license/redistribution status, entry points and test commands.
- Authentication, identity claims, audience, tenant/workspace mapping and authority attenuation.
- Capability version, manifest and provider build; allowed destinations and data disclosure.
- State owner, checkpoint model, consistency, idempotency window and ambiguous-outcome reconciliation.
- Rate/concurrency limits, timeout/cancellation behavior and cost accounting owner.
- Storage, retention, privacy, backup and redaction rules; whether metadata reveals private inputs.
- A clean reproducible provider test and a mapping from each returned receipt to its actual meaning.

An adapter maps an existing contract; it does not conceal incompatible semantics. If a provider lacks reconciliation, mark the operation unsupported for automatic retry. If no current-reader check exists, do not cache protected payloads under broad NexOS access. If a provider's model fallback could send data to another destination, reject it under a local-only grant.

## 5. Keeping the first product independent

The local control plane, broker and workspace shell must start without Kubernetes, Cikut, Temporal, Fuseki, Qdrant or a remote model endpoint. That constraint does not authorize cloning their complete functionality. Use exact local ownership for deterministic OS work and explicitly optional adapters for broader services.

If an existing component can be embedded or deployed locally within the resource budget, prefer that option after a measured integration spike. If it needs remote infrastructure, retain the boundary and make the remote feature unavailable offline. State what remains usable and what is waiting for connectivity. Do not silently queue a privacy-sensitive remote disclosure for later transmission unless the grant covers that behavior.

Rust is the proposed implementation default for the new broker and helper, not a mandate to rewrite RobotMind's Python services. Reuse stable protocols, SDKs or small out-of-process adapters. A language boundary has a cost; an unowned duplicate implementation has a larger continuing correctness cost. P00 records the actual choice and evidence.

## 6. Scope of the initial audit package

The earlier package treated every named component as an unverified candidate. This update identifies concrete source locations and already-existing boundaries, but intentionally keeps runtime qualification pending. P00 uses these observations to prioritize a bounded audit of the first integration path. P13 qualifies the broader ecosystem adapters; unrelated local product work can proceed while an external permission or deployment is unavailable.

No private source contents, credentials, Kubernetes secrets or live data are included in the archive. The observation manifest preserves exact source links and Git identities so authorized engineers can reproduce the investigation.
