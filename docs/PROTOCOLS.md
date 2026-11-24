# Protocol and provider contracts

Status: proposed normative wire profile `0.1.0`. The first implementation must make the local path work end to end before adding distributed transports. [Schemas](../contracts/nexos.schema.json) validate record shape; authorization, concurrency and provider behavior require implementation tests.

## 1. Transport, identity and bounded parsing

The reference local transport is length-prefixed UTF-8 JSON over a Unix-domain socket. Each frame begins with a 4-byte unsigned big-endian byte length. The initial maximum frame is 1 MiB; larger artifacts travel by scoped object references. Reject oversized frames before allocation, duplicate object keys, invalid UTF-8, non-finite numbers and unsupported protocol versions. Enforce request deadlines, per-principal concurrency and response-size limits. These are chosen initial limits, not benchmark results.

A connection is bound to a broker-established principal and an execution identity. OS peer credentials are evidence, not proof of distinct agents sharing one UID. Workers receive isolated identities and bound channels; client-supplied `principal_id` is an assertion checked against that channel. Enrollment and secret handoff are owned by a trusted component. Avoid reusable bearer secrets in request bodies, logs or generated views. The administrative endpoint is separate from worker invocation endpoints.

A browser shell uses a local authenticated bridge, origin checks and anti-CSRF measures. Binding a TCP listener to localhost is not browser authentication. A later remote adapter uses authenticated encrypted channels and node enrollment; it cannot broaden the local contract by replacing the transport.

## 2. Envelope and methods

A request envelope has `protocol_version`, `request_id`, `method` and `params`. `invocations.prepare` consumes a `preparation_request` without a digest or approval; it returns a broker-stored `prepared_action` plus its computed digest. `invocations.commit` consumes an `invocation` referencing that exact preparation. A response echoes `request_id` and has exactly one of `result` or `error`. A request ID correlates transport; an invocation ID identifies durable work. Reconnecting with the same request ID alone does not deduplicate effects.

| Method | Inputs and behavior | Authority consequence |
| --- | --- | --- |
| `session.hello` | Negotiate an explicitly supported protocol version and profile; return safe server capabilities. | Does not grant authority or expose inaccessible providers. |
| `capabilities.list` / `describe` | Paginated, authorized discovery of reviewed versions, schema references and profile status. | Discovery never auto-enables a tool. |
| `workspaces.get` / `resources.inspect` | Return current revision, managed scope and data freshness. | Read grants and disclosure policy apply. |
| `invocations.prepare` | Validate request shape, bind a manifest and resource revisions, compute effects and return a prepared action. | A preview is not a reservation or authorization guarantee; any mutating preparation must itself be a declared capability. |
| `invocations.commit` | Present the immutable prepared action, current grant and optional bound approval. | Rechecks policy and preconditions; atomically records admission/reservations in local state. |
| `invocations.get` / `receipts.list` | Observe durable status and effects under current read authority. | A former caller is not entitled to a result after access is revoked. |
| `invocations.cancel` | Request no further dispatch; attempt provider cancellation where supported. | Does not assert reversal of completed effects. |
| `grants.issue` / `revoke` | Issue narrower authority or advance revocation state. | Issuer authority, audience, parent chain, expiry and budgets are checked deterministically. |
| `events.subscribe` | Read authorized events after an opaque cursor with replay/dedup metadata. | Revalidate on delivery; revocation closes or narrows stream access. |

The schema bundle contains the envelope and principal operation records, not every method payload. P01 must specify any additional payload before exposing that method. Unknown methods and incompatible versions fail with a typed error, rather than being treated as free-form shell commands.

## 3. Capability registration

A capability is registered with exact semantic version, provider ID, provider build digest, input/output schemas, effect properties, authority requirements, idempotency/reconciliation semantics and qualification profile. Schemas describe valid structure; preconditions describe current state. Both matter. The v0 profile requires object-root input/output schemas. Registration rejects remote `$ref`/`$dynamicRef` resolution and embedded `$id` base changes. Proposed admission ceilings are 128 KiB per embedded schema, depth 32, 4096 nodes and 256 characters per regex. Production validation additionally needs a safe regex/evaluation strategy and wall-time limits; these structural limits alone do not prove resistance to computational denial of service.

Production dispatch requires a provider qualified for the requested scope. To establish that qualification, an explicitly authorized disposable test deployment may admit a candidate provider under a separate qualification policy. It uses test-owned resources, real containment enforced by the harness, and no production credentials; its receipts are labeled test evidence. This mode is selected by trusted deployment configuration, never a caller-supplied bypass flag. Candidate execution cannot self-mark the provider qualified.

A provider manifest is reviewed and pinned by digest. Changes in tool description, allowed destinations, effect semantics, inputs, compensation or provider build invalidate the applicable qualification/approval according to change class. A model cannot self-certify a tool as read-only. MCP tool annotations are untrusted hints unless a trusted server supplies them; NexOS requires its own evaluated provider binding. [MCP tools specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx).

Adapters map MCP, D-Bus, application APIs, CLI programs or native providers into the contract. They do not import ambient user credentials. Treat shell programs as explicitly bounded capabilities with argv arrays, declared cwd, sanitized environment, output limits and an OS sandbox. Do not interpolate model strings into a host shell. A legacy GUI adapter declares incomplete observability and recovery; it cannot assert semantic guarantees simply because the click completed.

## 4. Reviewed action binding

The `prepared_action` schema defines the complete hash preimage: capability ID/version/manifest digest, provider build, workspace and branch, exact input object, target resource/operation pairs and expected revisions, anticipated effects, allowed disclosure destinations, budget allocations and bounds, policy revision, qualification profile, deadline, validity interval, initiator and authority incarnation/epoch. The broker stores it immutably. An invocation references its ID and digest rather than sending a second mutable copy of the action; principal, task, grant, workspace, authority and deadline fields must match the stored preparation. A client-supplied digest alone is never trusted. The trusted UI renders these fields independently of model prose.

If policy requires a review, the approval references the prepared action digest, reviewer identity, approval expiry and allowed use count. Any material change to inputs, targets, revisions, destinations, effects or cost ceiling requires a new prepared action and any required approval. An ordinary editor may change managed bytes without passing through the broker. Before preparation and promotion, the provider must verify fresh content digests or application checkpoints and seal the candidate behind a quiescence or immutable-snapshot barrier. Watcher events and a metadata revision alone cannot prove that the reviewed bytes are unchanged. A cosmetic view change does not require reapproval. Existing scoped grants can authorize classes of routine actions without per-click confirmation.

The runtime computes `SHA-256(domain_separator || canonical_action_bytes)` using an audited implementation of the [JSON Canonicalization Scheme, RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html). The chosen domain separator is UTF-8 `nexos.action.v0` followed by a zero byte. Reject duplicate keys before canonicalization; store the exact canonical bytes used. Do not approximate JCS with a language's ordinary `sort_keys` option. The supplied spec validator checks schema shape and fixture relations, not cryptographic canonicalization; a cross-language digest-vector gate belongs in P01/P02.

## 5. Admission and execution

1. Authenticate the channel, validate bounded JSON, negotiate the version and verify the asserted principal binding.
2. Resolve the exact capability and provider profile; require it to be available and qualified for the requested operation, or admitted by the explicitly scoped disposable qualification policy above.
3. Check scope, target identities, source/disclosure policy, grant parent chain, authority incarnation and revocation epoch, deadline, expected object revisions and required approval. Each grant contains rules, each with its own capability/resource/operation/destination sets; the combinations within a rule are intentional, but lists from different rules must never be unioned into a cross-product. Every actual read, write and disclosure must be covered by an appropriate rule. Separate rules express read-input/write-output restrictions.
4. In one short local transaction, create or recover the invocation, reserve enforceable budget and persist dispatch intent. No model or network call runs while that transaction holds locks.
5. Immediately before each dispatch, recheck the effect boundary, grant/revocation and resource fence. Persist an immutable `dispatch_record` binding the provider build, prepared action, attempt, authority incarnation/epoch, target resource identities, target-enforced fence/lease (or immutable-read contract), request digest and idempotency identity. A revocation epoch is not a resource fence. The effect receipt references this record. For a provider that cannot enforce a target fence, `bounded_dispatch` records the explicit exposure policy and maximum in-flight count, with no fabricated fencing token. Revocation can stop new broker dispatches but cannot stop the already accepted provider request. Such an operation requires policy authorizing that residual exposure; it cannot qualify a profile promising target-side fencing or a hard spend ceiling the provider cannot enforce.
6. Dispatch through the isolated provider, then persist the observed outcome and separately versioned `usage_record` observations. Receipts reference those usage records. Estimated usage also remains unsettled or disputed in v0; an accounting-adjustment protocol requires a separately specified, authorized decision before it can release liability. Unknown usage remains unsettled or disputed and does not free its reservation; measured settlement must use the reservation's unit, currency and exponent. Late results must match invocation, attempt and fence.
7. Evaluate task acceptance using returned artifacts and external observations; the provider saying “success” is only one observation.

The local transaction covers local records. It does not atomically commit an email, remote API, file tree, service restart and kernel state. Follow [state and recovery](STATE-AND-RECOVERY.md) for promotion and multi-provider recovery.

## 6. Retry and unknown-outcome rules

A logical invocation has one immutable invocation ID and one fixed idempotency key. At admission the broker creates unique mappings for the invocation ID and for `(authority incarnation, workspace, principal, capability binding, idempotency key)`. Both map to the same stored action digest. Repeating the exact pair may recover the existing result; changing either identity while reusing the other is an `idempotency_conflict`, not a fresh operation. Provider dispatch keys are derived and stored once from that logical mapping and remain fixed within the provider's qualified retention window. The broker also records an input/action digest. A repeat with the same identity and different content is `idempotency_conflict`. A repeat with identical content can return the existing outcome only after checking current result-read authority; it cannot create fresh effects under an expired grant.

For `intrinsic` idempotency, reapplication must genuinely have the same permitted effect. For `provider_key`, record the provider's retention window and scope; replay beyond that window is not safe. For `none`, a timeout after dispatch enters reconciliation, never blind retry. “Not found” proves non-application only when the provider's contract makes that absence conclusive and any consistency delay has elapsed.

A successful remote effect followed by a local crash can leave an unknown outcome. Reconciliation queries may need a separate, narrowly scoped permission after the original grant expires. A reconciliation decision records who established it and from what evidence. Compensation also needs current authority and may fail.

Read-only operations can disclose data or spend money. Retry policy therefore applies to all operations, not only mutations. Monetary reservations remain unsettled while charge outcomes are uncertain; releasing them blindly can admit overspend.

## 7. Errors and event semantics

| Error | Meaning | Permitted next action |
| --- | --- | --- |
| `invalid_request` | Invalid shape, range or unsafe encoding. | Correct request; do not dispatch. |
| `unsupported_version` | No compatible explicit contract. | Negotiate a supported version or block adapter. |
| `permission_denied` / `grant_expired` / `grant_revoked` | Authority insufficient. | Request a justified scope change or continue unrelated work. |
| `precondition_conflict` | Resource, manifest, policy or action revision changed. | Refresh, replan and regenerate review where required. |
| `budget_exhausted` | Enforceable reservation cannot be made. | Use an authorized cheaper plan or request a new limit. |
| `profile_unavailable` | Required sandbox, hardware or provider guarantee missing. | Select an already qualified profile; never degrade silently. |
| `provider_unavailable` | Provider cannot currently accept work. | Retry only within its declared semantics and bounds. |
| `idempotency_conflict` | Same operation identity, different action. | Reject; create a distinct intentional operation. |
| `outcome_unknown` | Effect may have happened. | Reconcile; do not replay non-idempotent work. |
| `result_withheld` | Current authority cannot read the historical result. | Show only authorized metadata and recovery action. |

Events have an owner-local sequence, event ID, causal references and payload reference. Delivery is at least once; consumers deduplicate by event ID. Do not promise global ordering across owners. Export to OTel is a projection and can be sampled or lost without changing canonical operation outcomes. A receipt is not an OTel span, and absence of a trace is not proof of no action.

## 8. Declarative views and forms

The trusted resolver checks each `query` binding against the registered manifest; mutating operations are rejected as queries. Non-mutating operations still require disclosure and cost authorization. Initial query bindings run only on explicit user request or an already authorized refresh policy with bounded frequency/spend. Merely opening a generated view cannot grant authority or authorize repeated paid inference.

`binding.input` supplies initial parameter values. The `declarative-v0` renderer derives form fields from the registered object-root input schema, validates current edited values, and sends them through preparation. Editing a form after review creates a new preparation; it never edits a sealed action or carries its approval forward. A form/action component must reference an action binding. Text and labels render as inert text. The generated view cannot draw or impersonate the trusted authorization controls. Tables are derived from actual schema-described query outputs; later custom charts require a separately versioned renderer profile.

## 9. Versioning, secrets and federation

Store contract and provider revisions with every invocation and checkpoint. Bind grants and dispatch to a nonreused authority-incarnation ID as well as a monotonic epoch; restoring a backup rotates the incarnation and invalidates prior dispatch authority. An upgrade may read old state but must not silently reinterpret old authority. New unknown authorization fields fail closed; unknown informational extensions require a documented namespaced extension policy. The initial profile uses closed objects and explicit versions.

Provider secrets are resolved by trusted brokers under task-bound identity. Never pass a caller token blindly to an unrelated upstream: audience binding and delegation remain explicit. [MCP security guidance](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices).

The first federated workspace has one authoritative writer and target-enforced fencing. Offline nodes can operate on explicitly detached local branches with valid local grants; they cannot pretend to renew central authority. Read models and checkpoints may move, but target resources must validate lease/fence state before accepting effects. An unavailable authority is a real boundary, not a reason to mint a replacement lease.
