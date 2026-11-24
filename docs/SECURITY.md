# Security and authority

Status: normative design; no isolation profile is qualified by this document alone. This specification covers effects mediated by NexOS and the resources explicitly placed under its protection. A descriptive permission in a prompt is not enforcement.

## 1. Threat model and trust boundary

Protected assets include workspace contents, execution identity, provider credentials, budget reservations, effect receipts, recovery material and the user's ability to stop delegation. Threat actors include a malicious or mistaken agent, hostile task input, compromised worker code, an untrusted provider, a second workspace tenant, a stale remote executor and an application attempting to become a confused deputy.

The local host administrator, a compromised kernel/hypervisor and an attacker controlling the trusted owner login are outside the baseline sandbox guarantee. The owner can intentionally bypass NexOS using ordinary Linux administration; the system must disclose that activity as outside mediation when it can observe it. Defending against administrator compromise or physical device theft requires separately qualified boot, disk encryption, key custody and recovery policies. It cannot be inferred from application-level grants.

Do not classify an executable as safe because a model generated it, a package is open source or its instructions look benign. Treat external documents, terminal output, filenames, model responses and tool metadata as untrusted input. A model may propose a plan; deterministic policy decides whether each effect can be admitted and dispatched.

## 2. Principal identity is not a display name

Human principals, service principals and agent principals use the same typed capability interface but may hold different grants. The authenticated connection establishes identity. Fields such as `principal_id`, `workspace_id` or a claimed role inside a payload must not override that connection binding.

Local Unix socket peer credentials expose process credentials; they do not establish the identity of multiple mutually untrusted agents sharing the same UID. NexOS must bind each managed worker to a distinct execution context and a private channel or short-lived credential. Relevant isolation includes dedicated worker identities, restricted credential delivery, process visibility restrictions and no access to another worker's socket or inherited descriptors. Recycled numeric UIDs are not persistent principal IDs. [Linux unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html)

The owner interface must not offer an ambient "act as owner" endpoint accessible to all sandbox workers. A compromised ordinary process already running with the trusted owner session's full authority remains outside the narrower worker threat model; a UI label cannot repair that boundary. Administrative enrollment, grant elevation and recovery use a distinct authenticated control path.

Remote authentication binds a node/service identity to its credential and configured trust root. A remote node certificate identifies a node; it does not automatically authorize every resident agent or workspace. Enrollment and credential rotation are auditable capabilities with their own scope.

## 3. Grants and delegation

A grant identifies issuer, subject, allowed capability versions or families, resource selectors, allowed destinations, validity interval, budget references, delegation depth and revocation lineage. Authorization evaluates the full live parent chain. Resource selectors use canonical IDs resolved to handles at the effect boundary; a textual path prefix alone is insufficient.

Delegation must attenuate every relevant dimension: permitted operations, resources, destinations, lifetime, budget and further delegation. A child cannot reset a parent budget by issuing a new identifier. Child reservations consume the same accounted ancestor allocation, or an explicitly transferred suballocation that remains counted against the ancestor. Revoking or expiring an ancestor invalidates its descendants for future dispatch.

Grant possession does not prove that a provider is trustworthy or that an operation is reversible. The broker additionally validates capability registration, provider identity, the reviewed manifest digest, version and required isolation profile. New or changed providers cannot silently retain a previously approved contract while changing their effects. Tool annotations received from a provider are claims to evaluate, not security facts.

## 4. Effect classification is multidimensional

Use explicit axes rather than one category that mixes recoverability, cost and authorization:

| Axis | Contract values | Why it matters |
|---|---|---|
| Mutation | `none`, `managed_data`, `host_system`, `external_system`, `physical` | A read may still reveal private data or spend money |
| Reversibility | `not_applicable`, `reversible`, `compensatable`, `irreversible` | Determines available recovery, not authorization by itself |
| Idempotency | `intrinsic`, `provider_key`, `none` | Determines retry policy under declared scope and retention |
| Reconciliation | `supported`, `unsupported` | Determines whether an uncertain outcome can be established safely |
| Disclosure | `none`, `local_only`, `named_destinations` | Prevents "read-only" from implying harmless |
| Cost | `enforced_limit`, `bounded_estimate`, `unknown` | Determines admissibility under a hard budget |

The [domain model](ONTOLOGY.md) owns these field meanings. Resource identities and destination allowlists further constrain each operation. Missing classification cannot be upgraded to a favorable property by a model; incomplete manifests are rejected. A `bounded_estimate` is not an enforced ceiling.

For example, sending a document to an external model is a disclosure and possibly a charge even if no source file changes. Deleting a snapshot may be irreversible if it is the last recovery copy. Cancelling a purchase request does not undo a charge already accepted upstream. A provider policy must govern remote reads as well as remote mutations. The user-facing plan must expose these concrete consequences.

## 5. Enforcement profiles

Each execution records the actual qualified profile and feature probe results. Profiles are contract names, not marketing strength ratings.

| Profile | Boundary | Baseline use |
|---|---|---|
| Managed provider | Small trusted adapter with narrow credentials and typed operations | Files, journal queries, approved service integrations |
| OS sandbox | Separate worker identity; restricted mounts, namespaces, cgroups, syscall/LSM policy; no direct network by default | Bounded code in managed local workspaces |
| VM isolation | Dedicated guest boundary, restricted device model and controlled resource exchange | Higher-risk code when separately qualified |
| Legacy unmanaged | Ordinary host application under user control | Compatibility only; no strong mediation guarantee |

An OS sandbox shares the kernel with the controller. VM isolation changes the boundary and introduces a hypervisor/device-model trust base; it is not verified merely because development occurs inside a VM. Where the requested profile is unavailable, execution is unavailable. A diagnostic mode may explain missing primitives but must not execute the denied operation.

systemd provides many relevant execution and resource settings, but their availability and effect depend on kernel, manager mode and configuration. Some options have no effect when the required facility is absent. NexOS must probe and test outcomes rather than accept a successful service launch as proof. [systemd.exec](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) and [systemd.resource-control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html)

Landlock can add restrictions to a process and its descendants, but supported access rights depend on its ABI. Its network facilities are not a complete application-level destination policy. For a required guarantee, NexOS must require the needed ABI or another qualified enforcement mechanism; best-effort feature dropping is insufficient. [Landlock documentation](https://docs.kernel.org/userspace-api/landlock.html)

## 6. Prevent direct bypass

Workers cannot inherit the owner's home directory, SSH agent, cloud credentials, Docker socket, unrestricted D-Bus connection, runtime administration socket, writable control database or host device access. Mounts begin from an allowlist. Exported file handles and output directories are scope bound. Protect against symlink traversal, renamed parents, hard links, mount substitution and races between path validation and access. Directory-relative handle resolution with checked kernel facilities is a reference implementation technique; the provider must test escape cases. [openat2(2)](https://man7.org/linux/man-pages/man2/openat2.2.html)

Network access is denied by default. A connector that needs a remote service owns narrowly scoped credentials and mediates the request; arbitrary worker code does not receive a bearer secret granting broader access. Egress policy accounts for DNS rebinding, redirects, resolved addresses, loopback and link-local/metadata services, not only a string hostname supplied by the model. Endpoint allowlisting cannot by itself authorize arbitrary payload disclosure.

The privileged helper resolves managed resource IDs to preapproved operations. It must reject arbitrary unit properties, arbitrary executable paths and unvalidated command fragments. It uses expected revisions and active leases, and reports actual effects. An allowed `execute` capability must still name the executable/container contract, filesystem scope, resource limits and effect envelope; otherwise it is an unrestricted escape hatch.

## 7. Revocation, expiry and stopping

Revocation first commits a new authority epoch and prevents new admissions. Dispatchers must consult current authority at every effect boundary. For local mediated dispatch, the acknowledgement means that the local boundary has installed the revocation and will reject later dispatch attempts under that grant. It does not mean an earlier network request has been recalled or a worker has ceased all CPU activity.

The UI distinguishes revocation requested, enforcement acknowledged, process stop requested, process stopped and effects reconciled. Already dispatched effects may complete. Providers able to fence old epochs must do so at their commit boundary; providers unable to fence require bounded in-flight exposure and honest status. A long-running provider operation needs declared internal checkpoints or is one indivisible in-flight effect for this purpose.

For a disconnected node, immediate revocation is unavailable unless the node consults an online authority before each effect. Offline grants therefore have finite, explicit leases and exposure limits. A revoked remote grant is shown as pending enforcement until acknowledgement or lease expiry under the provider's tested clock/lease policy. Do not equate an elapsed client timer with proof that a remote actuator has stopped.

## 8. Resource and monetary authority

Admission reserves against the canonical budget before dispatch, using integer quantities with explicit units, currency and scale. Concurrent reservations must not exceed the enforceable envelope. A budget decrease below existing commitments prevents further admission and exposes those commitments; it does not rewrite past usage.

Enforced ceilings and estimated costs are separate. A local allocation may have a tested CPU/RAM policy, while an external model endpoint may expose only an approximate monetary quote. If a strict maximum is required and the provider cannot enforce or conservatively bound it, reject the request or require authority for an explicitly stated worst-case liability. Never claim exact spend protection from a token estimate alone. Unknown remote outcomes retain the reservation or an explicitly tracked unresolved liability until reconciliation.

## 9. Data, secrets and observability

Secrets are provider references delivered only to the credentialed adapter that requires them. They are excluded from prompts, default logs, demonstration capture and general artifact search. Restrict output access because model results and terminal output can also contain secrets. Authorized access to an input does not imply authority to send it to a different model or export it to another workspace.

The causal ledger stores minimal actor, grant, operation, status and evidence references. Sensitive payloads live in separately encrypted, access-controlled stores with retention and deletion rules. Hashes, filenames and causal relationships can themselves leak information; queries filter metadata as well as payload. A redacted or deleted item is represented explicitly, without preserving its secret text in an audit field.

OTel traces aid diagnosis but are not the security ledger: collectors can drop data, sampling can omit it, and user-controlled attributes are not authorization evidence. Captured explanations are claims by an actor, not authenticated introspection into its reasoning. Signed or hashed records establish limited integrity properties; they do not prove that recorded observations are true or resist a fully compromised administrator without an independent trust anchor.

## 10. Required adversarial qualification

Every qualified profile must demonstrate denied cross-workspace reads/writes, impersonation, parent-grant escalation, stale-token use, concurrent overspend, symlink/path escape, inherited-descriptor leakage, direct network bypass and use after revocation acknowledgement. Inject prompt instructions into file contents, provider descriptions and terminal output and show that no unauthorized effect follows. Kill processes around dispatch and receipt persistence, then verify no unsafe blind retry.

Tests run against real enforcement facilities on the declared platform tuple. Policy unit tests are necessary but cannot qualify OS isolation. Missing attack coverage or unknown provider guarantees remain visible gaps. Robot control additionally requires independently designed physical safety interlocks; this general runtime is not a real-time or safety-certified controller.
