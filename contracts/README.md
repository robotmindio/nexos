# Contract registry

Contract version: **0.1.0, proposed**. [nexos.schema.json](nexos.schema.json) uses JSON Schema Draft 2020-12. Its `.invalid` URI is an identifier, not a hosted endpoint. All schema resolution is local. [examples.json](examples.json) contains synthetic positive and negative fixtures, never actual grants or runtime receipts.

| Definition | Owns | What shape validation cannot establish |
| --- | --- | --- |
| `request`, `response`, `error` | Bounded transport envelope and known method names; prepare/commit payload shape. | Authentication, rate limits, exact framing or every future method payload. |
| `capability` | Immutable provider manifest: version, build, schemas, effects, idempotency and reconciliation requirements. | Provider honesty, sandbox safety, successful qualification. `requested_profiles` only requests evaluation. |
| `grant` | Exact capability bindings and correlated scope rules, destinations, authority incarnation, expiry and allocations. | Issuer's authority, revocation, attenuation or atomic budget reservation. |
| `preparation_request`, `prepared_action` | Separate client request and immutable broker-owned digest preimage, including branch, exact targets, cost, policy and authority. | Freshness, actual authorization, JCS implementation or provider effect bounds. |
| `invocation` | Durable identity and reference/digest for one exact prepared action. | Whether the binding is authentic, current authority holds or required approval exists. |
| `dispatch_record` | Attempt, provider build, authority incarnation and target fence/lease binding. | Whether a target enforces the fence or a network request actually left the host. |
| `usage` | Measured/estimated/unknown resource use, reservation link and settlement state. | Actual provider billing, reservation atomicity or enforceability of the ceiling. |
| `receipt` | One observed effect outcome and its evidence references. | Whether a provider lied, bytes exist, application is correct or every external effect is known. |
| `context_manifest` | Source custody, revision, freshness, purpose, classification and disclosure references. | Whether the reader remains authorized or external disclosure is lawful/approved. |
| `checkpoint` | Restore components, consistency declarations, pending invocations and current-authority revalidation. | Application consistency, recoverability, availability or completeness of bytes. |
| `view` | Constrained component and binding records. | XSS resistance, anti-spoofing, accessibility or correctness of displayed data. |
| `evidence` | Version/environment manifest/coverage/commands/result/limitations and restricted qualification claims. | Authenticity, reproducibility or independent verification of the recorded claim. |

A registry keeps qualifications separately, keyed by immutable manifest/build/profile. Do not put a mutable `qualified=true` claim into the manifest and then hash it: qualification would change the subject it supposedly qualified. A provider cannot mark itself safe by filling out a JSON field.

## Run the specification checks

Use Python 3.12 or newer. Install the exact validation dependencies from the repository root, then run:

```bash
python3 -m pip install -r requirements-spec.txt
python3 scripts/validate_spec.py --report evidence/spec-validation.json
python3 -m unittest discover -s scripts/tests -v
```

The commands validate the bundle, positive and negative fixtures, explicit semantic relationships within each fixture, program DAG, traceability, program state and local documentation links. The unit suite challenges the validator with corrupted plans, unsafe fixture fields and missing evidence. The output is specification evidence only. It cannot mark the runtime packages completed.

The optional report is a reproducible check result, not a signed attestation. It records the input-file digests and validator/tool versions. Re-run after modifying any canonical contract. Verification dependencies are needed locally; this archive does not vendor them or a NixOS image.

## Parsing and semantic validation obligations

Implementations MUST reject duplicate JSON keys before schema validation. Shape checks use a format checker rather than treating `format: date-time` as a decorative annotation; the official [validation specification](https://json-schema.org/draft/2020-12/json-schema-validation) distinguishes annotation and assertion behavior.

Beyond shape, the supplied fixture linter checks bounded relationships: grant validity interval, unique allocation IDs, context timestamps/token estimates, declared view bindings and evidence command exit expectations. These rules are an executable subset of the prose, not a production policy engine. Cross-record authority and state transitions remain implementation acceptance obligations.

Embedded capability input/output schemas are independently checked as schemas. They are standalone documents and must not accidentally reference the outer contract bundle. Avoid remote schema fetches. Explicit P00/P01 contracts must bound schema size, recursion and complexity before accepting third-party manifests.

## Meaning of the fixtures

Examples with repeated `a` or `b` digests are deliberately synthetic; they are not cryptographic test vectors. Each case is independent. A grant example permitting a write does not authorize the separate context-read example. P01/P02 must add real canonicalization vectors, matching request/receipt chains and current-state authorization tests before exposing operations.

The local validator does not implement SHA/JCS action binding, OS isolation, issuer authentication, checkpoint restore, provider idempotency or network controls. Those are required engineering work, explicitly referenced in the scenario matrix.

## Contract decisions deferred to implementation

The first package must freeze exact payloads for registry, workspace and event-stream methods, storage migrations and bootstrap policy in its ADR and tests. Later packages add their types only when an integrated experience requires them. This limits premature ontology growth while keeping future capabilities within the same authority and effect model.
