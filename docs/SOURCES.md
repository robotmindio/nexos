# Technical source register

Reviewed on 2026-11-24. These are primary sources supporting the narrow upstream facts used by the proposal. They do not establish that composing these facilities produces a correct or secure NexOS implementation. Architectural choices, proposed limits and product hypotheses are explicitly design judgments.

| Source | Narrow fact used | Design implication |
| --- | --- | --- |
| [NixOS manual](https://nixos.org/manual/nixos/stable/) | Declarative system configuration, generations, VM/image construction and service-specific migrations. | Use a reference test environment; treat mutable data compatibility separately from generation activation. |
| [Btrfs subvolume documentation](https://btrfs.readthedocs.io/en/latest/btrfs-subvolume.html) | Snapshot/subvolume semantics, nesting and shared storage blocks. | Enumerate managed scope and use independent backups; application consistency remains a provider obligation. |
| [SQLite WAL](https://sqlite.org/wal.html) | Local shared-memory WAL, a single writer, checkpoint/synchronization behavior. | One local authority transaction domain; no shared WAL across federation nodes. |
| [SQLite online backup](https://www.sqlite.org/backup.html) | Supported database backup interface. | Preserve a consistent database image instead of copying a live file without its journal state. |
| [systemd execution environment](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) | Execution isolation settings and host-dependent support. | Probe and test the effective boundary; a configured option is not sufficient evidence. |
| [systemd resource control](https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html) | Resource controls backed by cgroups. | Compile explicit limits and observe enforcement under load. |
| [Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) | Controller semantics and differing memory pressure/limit behavior. | Keep admission/accounting distinct from the kernel's actual enforcement mechanisms. |
| [Linux Landlock](https://docs.kernel.org/userspace-api/landlock.html) | ABI-dependent restriction of ambient rights. | Optional defense in depth after feature checks; not an all-purpose semantic authorization system. |
| [Unix-domain sockets](https://man7.org/linux/man-pages/man7/unix.7.html) | Peer-credential semantics. | Bind individual execution identities; shared UID alone does not identify a semantic agent. |
| [openat2](https://man7.org/linux/man-pages/man2/openat2.2.html) | Constrained directory-relative path resolution. | Resolve managed resources securely and test symlink/traversal races. |
| [KVM API](https://docs.kernel.org/virt/kvm/api.html) | Virtualization API and capability discovery. | Treat KVM as a substrate, requiring a VMM and a separately qualified worker profile. |
| [JSON Schema validation](https://json-schema.org/draft/2020-12/json-schema-validation) | Structural validation and distinction between format annotation and assertion. | Use format assertions and additional semantic checks; do not confuse schema validity with authorization. |
| [RFC 8785: JCS](https://www.rfc-editor.org/rfc/rfc8785.html) | Canonical JSON for stable hashing/signing inputs. | Use a qualified canonicalization implementation; ordinary language-level sorted JSON is not the normative algorithm. |
| [MCP tools specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx) | Tool schemas and trust limitations of annotations. | A discovered tool's read-only/idempotent labels are not security guarantees. |
| [MCP security guidance](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices) | Confused-deputy, token passthrough and related trust-boundary concerns. | Keep provider audiences, delegation and per-client authority explicit. |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Testable accessibility success criteria for web interfaces. | Use as a target for the applicable shell surfaces, not as a claim of tested conformance. |

## Project-specific source evidence

[Integration observations](integration-observations.json) records the exact RobotMind commit, paths and Git blob hashes inspected for this revision. [INTEGRATION.md](INTEGRATION.md) separates documented capabilities from source observations and missing runtime proof. Those private sources remain accessible only to authorized repository readers; their contents are not redistributed in this archive.

Upstream documentation URLs can move and stable manuals can advance. Implementation must retain exact source/build revisions and qualification evidence for its selected environment rather than relying on this dated review as a permanent compatibility certificate.
