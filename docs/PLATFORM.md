# Platform and distribution qualification

Status: selected target shape; no tuple is qualified yet. This document separates a portable runtime, its test environment, and a distributable operating-system image. Choosing a reference environment is not evidence of hardware support.

## 1. First target

The first qualification target, **Q0**, is a local x86_64 Linux host using KVM/QEMU to run a pinned NixOS guest. Inside the guest, NexOS manages one Btrfs workspace volume and CPU-only jobs under the OS sandbox profile. It has no cloud dependency, no GPU/NPU passthrough, no physical actuators and no general network access for workers. A deterministic local provider supplies the first real effect.

The guest is a repeatable test environment. It does not prove that each worker has a separate VM boundary. VM-per-worker execution requires a separate profile and qualification. If nested virtualization is unavailable, do not pretend that Q0 supports that profile.

| Tuple dimension | Q0 decision | Evidence required before execution claims |
|---|---|---|
| Architecture | x86_64 | Host/guest architecture and CPU flags |
| Host substrate | Linux with usable KVM | Host kernel build, `/dev/kvm` access and feature probe |
| Virtualization | QEMU with KVM acceleration | Exact QEMU build, device model and launch manifest |
| Guest | Supported stable NixOS release selected in P00 | Immutable nixpkgs commit, Nix/toolchain versions, kernel and image digest |
| Storage | Dedicated Btrfs managed volume; local SQLite control store | Kernel/progs versions, mount features, virtual disk cache/flush policy |
| Worker isolation | Qualified OS sandbox inside the guest | Actual UID/channel binding, namespace, cgroup, syscall and LSM tests |
| Resources | CPU only; reference test envelope of 4 vCPU, 8 GiB RAM, 40 GiB virtual disk | Provisioned limits and measured use; envelope is a test choice, not a minimum-product claim |
| Network | Worker egress denied | Direct bypass, loopback and inherited-socket negative tests |
| Inference | Disabled for core qualification | Core scenario completes with model endpoint unavailable |
| Data | One declared project tree plus supported job/checkpoint state | Explicit included/excluded resource manifest |

P00 resolves real versions and digests from available trusted sources, commits the lock/manifest and records boot evidence. Empty or invented hashes cannot satisfy that gate. Until then, Q0 is a defined target with unresolved pins. A successful run on one tuple does not qualify a different kernel, storage backend, CPU architecture or isolation policy.

KVM exposes VM and virtual-CPU facilities through its kernel interface, including capability discovery. NexOS must query supported features and use an established VMM instead of interpreting the presence of `/dev/kvm` as a complete machine-management solution. [KVM API documentation](https://docs.kernel.org/virt/kvm/api.html)

## 2. Capability matrix, not a universal Linux promise

| Environment/profile | Intended status | What must be proved separately |
|---|---|---|
| Q0 NixOS guest / CPU / Btrfs / OS sandbox | First implementation target | Local vertical experience, recovery and denial paths |
| Ordinary supported Linux distribution with package install | Runtime portability target | Dependency packaging, privilege setup, kernel features and storage adapter |
| Non-Btrfs managed workspace | Later adapter target | Equivalent isolation/checkpoint semantics and full-copy cost if used |
| VM-isolated worker | Later security profile | Guest escape boundary, VMM lifecycle, device minimization and resource exchange |
| GPU/NPU worker | Later accelerator profile | Drivers, model runtime, memory ownership, reset behavior and accounting |
| Two-node workspace federation | Later distributed profile | Identity, leases, fencing, partitions, checkpoint transfer and stale results |
| ARM laptop/SBC or robotics device | Later hardware profile | Boot/drivers, resource limits, thermal behavior and physical safety boundary |
| Windows/macOS host | No initial support claim | Different substrate adapters and enforcement semantics |

The runtime may discover that a requested feature is unavailable. It returns the supported subset and the reason, rather than weakening a required isolation or recovery property. Capability probes are not qualification by themselves: detecting Btrfs, for example, is not evidence that the chosen application can recover from a snapshot.

## 3. Why keep NixOS as the reference

NixOS gives a declarative system configuration, built generations and tooling useful for repeatable test images and configuration recovery. These are relevant inputs to managed environments. Its manual documents system builds, image generation and configuration switching, alongside separate service migration procedures. [NixOS manual](https://nixos.org/manual/nixos/stable/)

The product trade-off is operational complexity: Nix packaging and deployment conventions require expertise, and compatibility with arbitrary prebuilt software needs explicit treatment. NexOS should therefore expose ordinary concepts such as workspaces, previews and recovery to users, while keeping Nix an implementation provider. Do not make learning the Nix language a requirement for creating a task.

NixOS remains replaceable at the runtime boundary. The initial distribution avoids a kernel fork and reuses an established Wayland desktop/compositor. A custom shell can be a normal application or session integration before the team undertakes window management, accessibility plumbing, input methods, screen sharing and display-driver support.

## 4. Installation and lifecycle

The first runtime package must have a reversible installation path, explicit service identity, bounded state directories and a removal/export procedure. Installing NexOS must not silently take control of the entire home directory, copy private credentials into its store or start capturing all application input.

A later reference image has additional obligations: boot and recovery, user provisioning, disk layout/encryption policy, update verification, key rotation, retained rescue generation, supported hardware matrix and tested rollback with data compatibility. Full-disk encryption and secure boot may be supported features, but no assurance is claimed until their enrollment and recovery flows are tested on named hardware.

Builds and releases retain source revisions, dependency locks, build recipe, artifact digests, dependency/license inventory and the exact qualification results. These records support review; a hash alone does not establish trusted origin. Independent verification should build or verify from pinned inputs and boot a clean image. Distribution policy and licensing choices must be recorded before public release, while local design and implementation can proceed.

## 5. Operational cost and opportunity cost

Measure idle resource use, storage growth, checkpoint time, branch-copy cost, startup latency and recovery duration on Q0 before setting product performance promises. A general workflow service, semantic index and local model can each dominate a small machine; making all of them mandatory would defeat local autonomy.

Prefer optional integrations and one control daemon over a mandatory cluster. Keep full-copy branching as a truthful slower capability where snapshots are unavailable rather than requiring users to repartition before seeing product value. Delay driver work, a compositor, an app marketplace and generic multi-node scheduling until a complete local experience demonstrates their need.

Revisit a platform choice using a recorded failing scenario, not an abstract score. NixOS can be replaced as the first end-user distribution if compatibility or packaging costs outweigh its reproducibility advantages while the portable contracts remain intact. Linux kernel changes require measured unmet requirements, an upstream strategy and a maintenance owner.

## 6. Qualification record

Every claimed supported configuration must record the complete tuple above, test command and exit status, source/contract revisions, fault model, successful and failed cases, artifact digests, independent verifier and exclusions. Performance results include resource allocation and workload size. Security results name the exact profile and enforcement features.

A booted VM, a schema-valid manifest and a successful unit test are different pieces of evidence. None substitutes for the others. The program may publish an experimental runtime once its declared local profile is qualified; it need not wait for every future accelerator, federation or robotics feature.
