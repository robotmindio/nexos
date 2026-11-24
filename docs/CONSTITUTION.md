# Constitution

Status: proposed normative baseline. NexOS makes persistent work, bounded authority and inspectable effects available to humans, deterministic programs and model-driven agents.

## Principles with consequences

| Principle | Required consequence | Unacceptable shortcut |
| --- | --- | --- |
| Work has identity | Workspaces and tasks persist independently of UI, model session and process. | A transcript or PID as the sole task record. |
| Human control | People inspect targets, intervene, cancel future work, revoke authority, recover and export. | Making the human guess whether an agent is still acting. |
| AI-independent foundation | Core workspace, authorization, direct manipulation and recovery work without inference. | Claiming model-dependent planning still works with no model. |
| Real AI-native capability | Models discover structured operations, obtain authorized context, adapt persisted plans and are evaluated by outcomes. | Calling a deterministic workflow adaptive or fluent output complete. |
| Shared operations | Humans, CLI programs, UI and agents share capabilities with separately authenticated authority. | Giving an agent the full standing authority of its user. |
| Authority is enforced | Broker and OS boundary check grants, data destinations, budgets and revocation independently of model output. | Prompts or tool descriptions as access control. |
| Honest durability | Work declares checkpoint, retry and reconciliation semantics; unknown outcomes remain unknown. | Arbitrary process migration or general exactly-once external effects. |
| Honest reversibility | Revertible state is named; effect properties are independent; promotion declares real commit boundaries. | Presenting config rollback as rollback of data, messages or physical actions. |
| Evidence before assertion | Receipts identify actions, authority, versions and result confidence; summaries link to records. | Reconstructing convenient causal stories or recording private model reasoning. |
| Local ownership | Local boot and deterministic work need no remote identity, knowledge or inference service. | Requiring the RobotMind cluster to open a local workspace. |
| Compatibility with boundaries | Existing apps remain useful; managed and unmanaged activity are visibly distinct. | Claiming legacy software automatically obeys semantic grants. |
| Reuse with one owner | Reuse qualified services and give authoritative state one owner per domain. | Another Bifrost, generic workflow engine, identity provider or mirrored truth store. |
| Privacy by design | Context capture is scoped, inspectable, purpose-limited and removable; read permission does not imply model disclosure permission. | Global surveillance, silent private embeddings or cross-tenant cache reuse. |
| Composition and portability | Providers and views have versioned contracts; work exports preserve documented state. | Hiding long-lived work inside a model vendor's session. |
| Bounded complexity | Start with a modular local runtime, narrow helper and isolated workers. | A daemon, database or deployment per concept. |

## Boundaries

These requirements cover operations mediated by a declared NexOS profile. A hostile host administrator, compromised kernel or adversarial firmware is outside the first profile. Append-only records do not defeat these adversaries. Providers declare additional exclusions and remain unavailable when their required boundary cannot be established.

Ordinary apps may edit files outside managed branches. Those edits do not acquire causal history, rollback guarantees or semantic authorization by proximity to a NexOS window. Resource enrollment is explicit and names a consistency contract.

The kernel retains CPU scheduling and kernel resource management. NexOS adds admission and policy for tasks, inference and cost; it does not replace the mature kernel scheduler with a language model.

## Development consequences

The whole vision remains a direction; distant capabilities need not block a useful release. Qualification is per milestone, platform, provider and threat model. Robotics, broad hardware support and federated authority require their own evidence.

Reuse requires inspection and justification, not a veto on local work until every remote service is accessible. A local task journal is necessary system state and must not become a competing generic orchestration product. A local artifact index records owned bytes and must not redefine NoemaDB's epistemic model.

Follow the existing owner mandate. Escalate only when missing authority, unavailable access or a substantive trade-off prevents the assigned outcome. Routine engineering choices do not need repeated confirmation. Conformance obligations are tracked in [the invariant matrix](../conformance/matrix.json); usability and quality claims also require evaluation with observed outcomes.
