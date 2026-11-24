# NexOS

**A persistent operating environment for human and agent work.**

NexOS makes workspaces, bounded delegation, recoverable execution and inspectable effects first-class resources. People can use ordinary applications, manipulate state directly, compose typed capabilities or delegate to a model-driven agent within the same work context.

The reference direction is upstream Linux with a portable user-space runtime. NixOS supplies the initial reproducible qualification VM and a later reference distribution. The first product is a useful managed project workspace; the long-term architecture also supports generated interfaces, reusable procedures, federated compute and separately qualified physical-system adapters.

## What is in this repository

This repository contains the engineering specification, execution program and two NixOS live editions for VM development. The specification validator checks schemas, examples, dependencies, requirement coverage, evidence records and documentation references. The NexOS runtime is still pending.

| Area | Start here |
| --- | --- |
| Vision and value beyond AI | [Vision](docs/VISION.md), [opportunity costs](docs/OPPORTUNITY-COSTS.md) |
| Product and interaction | [Product design](docs/PRODUCT-DESIGN.md), [ten experiences](docs/USER-EXPERIENCE.md) |
| Actual AI-native behavior | [AI-native runtime](docs/AI-NATIVE.md) |
| Requirements and document ownership | [Constitution](docs/CONSTITUTION.md), [specification rules](docs/SPECIFICATION.md) |
| Architecture and recovery | [Architecture](docs/ARCHITECTURE.md), [state and recovery](docs/STATE-AND-RECOVERY.md), [platform](docs/PLATFORM.md) |
| Authority and protocols | [Security](docs/SECURITY.md), [ontology](docs/ONTOLOGY.md), [protocols](docs/PROTOCOLS.md) |
| Machine-readable contracts | [Contract registry](contracts/README.md) |
| Existing RobotMind integration | [Verified source discovery and remaining gates](docs/INTEGRATION.md) |
| Engineering sessions | [AGENTS.md](AGENTS.md), [start mandate](program/START-HERE.md), [execution procedure](program/EXECUTION.md) |
| Program and acceptance | [Program](program/PROGRAM.md), [plan](program/plan.json), [state](program/state.json), [conformance](conformance/ACCEPTANCE.md) |
| Review findings, in Spanish | [Exhaustive proposal review](audits/REVIEW-2026-11-24.es.md) |
| Primary technical sources | [Source register](docs/SOURCES.md) |

## First integrated result

Create a managed workspace, run a real typed operation under bounded authority, inspect its receipts, branch managed state, validate/promote a change, interrupt/recover a task and resume from a persistent shell. Core use remains available with inference disabled. A separate AI milestone adds a real model, authorized context, adaptive plans and independently verified outcomes.

This delivers a concrete product while preserving the wider vision. Generated views, demonstration learning, reference-image lifecycle, federation and accelerated hardware extend independently qualified profiles. They are not all prerequisites for a local-runtime release.

## Build and boot the live ISOs

On an `x86_64` Linux host with Nix installed, run the build script for the edition you want. [nexos.nix](nexos.nix) defines the shared settings and package list, starting with Git. The Plasma edition adds KDE Plasma 6 and its KWin Wayland compositor through the [Plasma module](profiles/plasma.nix). Both editions use the Nixpkgs revision in [flake.lock](flake.lock).

```bash
./build-iso.sh console    # result/iso/
./build-iso.sh plasma     # result-plasma/iso/
```

Running `./build-iso.sh` without arguments builds the console edition. Boot either image in a VM with QEMU and access to `/dev/kvm`.

```bash
qemu-system-x86_64 -enable-kvm -smp 2 -m 2048 -nic none -cdrom result/iso/*.iso -nographic
qemu-system-x86_64 -enable-kvm -smp 2 -m 4096 -nic none -vga virtio -cdrom result-plasma/iso/*.iso
```

Run `git --version` in the console or in Konsole on the Plasma desktop. To leave QEMU in console mode, press `Ctrl+A` followed by `X`.

## Install an edition to disk

Boot the desired edition and use the [NixOS manual installation steps](https://nixos.org/manual/nixos/stable/#sec-installation-manual) to prepare and mount the target filesystem at `/mnt`. Once the target filesystems are mounted, generate the host configuration and copy the edition modules from the live system.

```bash
sudo nixos-generate-config --root /mnt
sudo install -m 0644 /etc/nexos/install/*.nix /mnt/etc/nixos/
```

Add `./edition.nix` to the `imports` list in `/mnt/etc/nixos/configuration.nix` alongside `./hardware-configuration.nix`. Finish configuring the bootloader and user accounts for your machine, then run `sudo nixos-install`. `edition.nix` imports the shared package list in both editions and also imports the Plasma module when installing from the Plasma ISO.

The [initial ISO smoke test](evidence/iso-smoke.md) records the original single-edition build and hostname check.

## Verify this package

From the repository root:

```bash
python3 -m pip install -r requirements-spec.txt
python3 scripts/validate_spec.py --report evidence/spec-validation.json
python3 -m unittest discover -s scripts/tests -v
```

The checked-in report records the inputs checked and tool versions. Re-run it after edits. The 15 engineering packages and seven release profiles remain pending; successful specification checks do not change those states.

## Begin implementation

Use [the bounded M1 mandate](program/START-HERE.md), then [AGENTS.md](AGENTS.md). P00 resolves the actual target pins and the first integration contract. P01 immediately exercises a real operation rather than delivering empty services. Continue through the assigned milestone without stopping at each commit; preserve exact checkpoints when a session must end.

The first qualification target is a CPU-only x86_64 Linux/KVM/QEMU environment with a NixOS guest and explicitly managed storage. The live ISO provides the guest for initial development. P00 also covers the runtime toolchain, storage and integration contracts.

## Project status and licensing

Specification version `0.1.0`, reviewed 2026-11-24. Architecture decisions are proposed implementation defaults with measured revisit gates. The source repository is public at `robotmindio/nexos`. Licensing and distribution of built images remain owner-selected decisions.
