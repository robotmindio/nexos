# Qualification and evidence policy

Status: normative. Runtime experiences and invariant tests are not yet implemented. The included specification checks validate documents, schemas and examples only. They must never update a package or profile to `qualified` by themselves.

## 1. Distinct claims

| Level | What it establishes | What it cannot establish |
|---|---|---|
| Specification validation | Parseable schemas/examples, valid IDs, graph/reference consistency and declared contract rejection cases. | OS behavior, security, runtime correctness or integration. |
| Unit/model checking | Behavior of a bounded implementation/model under controlled inputs; doubles are allowed and identified. | Real provider, kernel, persistence or network semantics unless actually exercised. |
| Component integration | Real participants at the tested boundary and environment. | Untested end-to-end product behavior. |
| Experience qualification | A positive path and its required negative/recovery paths on a pinned revision and tuple. | Other variants, models, hardware, threat models or universal correctness. |
| Release-profile qualification | Independent reproduction of the profile's prerequisites and integrated behavior, lifecycle and limitations. | Other profiles or the entire roadmap. |

Package qualification is scoped to `program/plan.json.packages[].qualification_kind`. P00 is `specification`: its independently reviewed inventory, contracts and reproducible environment setup can qualify that engineering deliverable without claiming NexOS runtime behavior. P14 is `engineering`: its qualification procedure/tooling can be verified independently without claiming every release profile. P01–P13 are `runtime` and require real runtime/integration evidence for their advertised capabilities. Every release profile also requires real runtime evidence. A bundled specification-validator report by itself does not establish P00's complete acceptance, and no non-runtime record may qualify a runtime package or release.

All kinds require genuine, non-example, passed records bound to the exact package acceptance scope and independently verified. The field `qualifies_runtime` remains false for a non-runtime claim; it is not forced true merely because an engineering package is qualified.

An implemented runtime can have incomplete qualification. Missing evidence is not a pass. A mock is useful in a unit test but cannot substitute for the provider in a provider claim. A real local test service may qualify the local-service contract; it does not qualify a different SaaS API.

## 2. A qualification tuple

Every runtime result identifies source commit and dirty-tree/patch digest if any; contract/schema versions; target architecture and OS/kernel build; image or environment digest; filesystem/persistence settings; required sandbox facilities and privileges; compiler/runtime dependencies; provider/API revisions; model/build/settings when relevant; hardware/driver/runtime for accelerators; network topology and lease/clock assumptions for federation; configuration/policy and fixture input digests; and data/migration versions.

Use exact observed values. Unknown tuple components remain unresolved and restrict the claim. P00 pins the first tuple; the specification does not invent it. A release qualification targets a clean reproducible revision, while a dirty-tree exploratory result must be labeled and cannot silently transfer to a later commit.

## 3. Evidence bundle

Retain the claim/profile and experience/invariant IDs, actual commands, working directory, environment references, timestamps, exit codes, required logs, before/after observations, artifact/receipt digests, negative outcomes, fault-injection point, recovery result, limitations and verifier identity/result. Store only authorized/redacted payloads. A receipt links authority and effects but need not publish secrets or private inputs.

Use [contract definitions](../contracts/README.md) for machine-readable records and their known limits. Schema validity does not prove record authenticity. The evidence's source revision must match the submitted implementation or carry an explicit accepted impact assessment; a broad `tests passed` sentence is insufficient.

No successful runtime evidence is included in this design package. Generated example records are synthetic contract fixtures and must remain labeled as such. Real evidence belongs under [evidence/](evidence/README.md) or a durable authorized artifact store referenced with integrity metadata.

## 4. Negative checks and crash boundaries

At minimum test invalid authority, identity confusion, delegation amplification, expired/revoked grants, direct boundary bypass, stale revisions, conflicting promotion, concurrent reservations, resource exhaustion and unsupported contract versions where applicable. Test the real boundary, not only a policy function that returns `false`.

For durable effects, inject failure before dispatch intent persistence, after durable intent but before dispatch, after external dispatch before response, after response before receipt durability, and during settlement/recovery. Verify the actual persistence and provider semantics. Do not assert universal exactly-once execution. For snapshots, identify crash consistency versus application consistency and validate the relevant restore path.

For AI, use actual named model calls for the AI claim, independently checked artifacts and adversarial/stale context. Do not count the model's self-assessment as the success oracle. For isolation, use a real adversarial worker and verify target state. For federation, exercise actual network faults and stale commits at enforcing resources.

## 5. Independent reproduction

The author produces the recipe and marks work implemented. A different agent/person reproduces package-critical positive and negative checks against the pinned submission. It inspects fixtures, environment identity and scope instead of accepting a summarized pass. Independence means separate execution/judgment, not a claim of formal assurance.

If no verifier is available, leave work implemented and identify the outstanding qualification. A qualified result is invalidated by material changes to the tested code, contracts, policy, provider or tuple; use impact-based reruns rather than either stale blanket acceptance or automatic full-suite repetition.

## 6. Profile eligibility

`program/plan.json.release_profiles` is the canonical prerequisite list. A profile may qualify only when every required package is qualified, its exact experience variants and relevant invariant obligations pass, P14's qualification procedure is implemented, and the independent verifier has accepted the profile evidence. Dependency closure must also be satisfied. An explicitly permitted implementation-only dependency is never enough for a claimed enforcement boundary.

P14's package qualification, if recorded, refers only to its engineering procedure and tooling. It does not substitute for profile evidence. P14 is not a universal release boolean. Track results under `program/state.json.profiles[profile_id]`. Its package work may remain implemented while individual profiles qualify. M7 means a named profile qualifies, not that all packages P00–P14 or all features exist. Multiple profiles at a version can have different states.

Contributor lists in the conformance matrix describe responsibility across baseline and extension variants. They are not an AND-gate requiring all future contributors before a baseline experience can run. The profile and experience variant supply that gate. Any claim of a richer variant must explicitly add its dependencies and tests.

A local-runtime release includes installation, runtime/data upgrade, backup/restore, compatibility and accessibility checks. It does not claim bootloader/image recovery. E10's reference-distribution variant additionally requires P11. A release may not omit a critical failing check and still call the same profile qualified.

## 7. Measurements and acceptance thresholds

Capture a conventional-Linux baseline for the same task, inputs, user skill and hardware. Measure task completion, user interventions, recovery/resume time, latency, idle CPU/RAM/storage, branch/promotion overhead, model spend and policy-denied effects. Report sample count, distribution and workload rather than a single attractive number.

Performance thresholds are set before optimization using the baseline and intended use; this package does not invent empirical budgets. Semantic safety gates are binary within the test: an observed unauthorized effect, stale fenced commit or secret leak is a failure. A finite absence of observed failures is evidence, not a universal security proof.

For AI success rates, use a fixed task set with defined postconditions and report failures, seeds/settings and model/provider versions. Avoid training or tuning directly against the final held-out qualification cases without disclosing it. UI feedback must include direct-manipulation, interruption and error-recovery tasks, not only a staged happy-path demo.

## 8. What remains to be implemented

The experience documents specify Given/When/Then behavior and negative paths. Each owning package must add actual executable runners, fixtures and fault-injection hooks appropriate to the implementation. There is deliberately no fake `nexos` binary, fabricated test transcript or empty pass-all harness. Specification validation is the only executable qualification level delivered at this stage.
