# ADR 0003: Operational state, derived knowledge and immutable actions

Status: proposed implementation baseline. Scope: first local runtime.

## Decision

Use one local authority store for grants, reservations, invocation/dispatch receipts and workspace generation metadata. The reference implementation is a modular Rust runtime with SQLite WAL on local durable storage. Keep the privileged OS helper narrow. Integrate existing external services through typed boundaries; do not rewrite RobotMind's services into Rust merely for language uniformity.

Separate operational truth from OTel traces, embeddings, knowledge projections and model summaries. Recuriant owns delegated workflows once admitted; Knowledge owns its epistemic contracts; Bifrost owns provider routing. A new local worker journal handles the exact OS operations the local runtime owns, not a parallel generic workflow product.

Store a prepared action immutably and hash its complete typed preimage with a qualified JCS implementation. A commit references that object. Mutable qualifications are indexed separately by manifest/build/profile and do not alter the manifest they qualify. Grants preserve permission correlations through explicit rules. Restore creates a fresh authority incarnation in addition to monotonic epochs.

## Alternatives and costs

A distributed database would ease some future replicated queries but imposes quorum/partition/operational costs before a local product exists. A fully event-sourced system adds replay and migration obligations; initially journal effects durably and use transactional current state plus a write-ahead outbox. A central semantic graph as the authority store would couple low-level safety to knowledge infrastructure and complicate offline operation.

Rust adds integration/FFI overhead where existing services are Python or TypeScript. Prefer out-of-process existing adapters and measure the boundary; P00 can revise this default through a documented evidence-based ADR. SQLite's single-writer limit requires short transactions and bounded work; no model call or remote I/O occurs while a state transaction is locked. See [architecture](../ARCHITECTURE.md) and [protocols](../PROTOCOLS.md).

## Revisit trigger

Revisit storage or process topology only after a measured workload exceeds the local writer/concurrency budget, a trust boundary requires process separation, or an existing embeddable owner demonstrably meets the contract at lower total cost. Require a migration path and one new canonical owner, not indefinite dual writes.
