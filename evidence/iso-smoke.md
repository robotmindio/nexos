# Live ISO smoke test

Built and booted on 2026-11-24 from source commit `6624b9b2460819090b4fd3f2146b7dfaab82cbda`. The baseline used a clean clone. The second clone changed only `networking.hostName` in `nexos.nix`. Both builds used Nixpkgs `0dc498bfe49baeb18b0f9891e800b53bb2603193` from `flake.lock`.

The `x86_64-linux` host ran Ubuntu 24.04.5 LTS, Linux `7.0.0-43-generic`, Nix `2.34.4` and QEMU `8.2.2`. Both guests ran NixOS `26.05.20261122.0dc498b (Yarara)` with Linux `6.18.64`. The guests used KVM, BIOS, two virtual CPUs and 2048 MiB RAM, with no NIC or persistent disk attached.

| `networking.hostName` | `hostname` in guest | `/etc/nexos-release` | ISO SHA-256 |
| --- | --- | --- | --- |
| `nexos` | `nexos` | `NAME=NexOS`, `HOSTNAME=nexos` | `0721ce67399fd3c937b3f8436de185a13674323d1eebdb5e7de36e229743266e` |
| `nexos-config-check` | `nexos-config-check` | `NAME=NexOS`, `HOSTNAME=nexos-config-check` | `60d7833b218c8b92ba13cad069dcd4bb674075381311fdaaa1e9d61dd8312b75` |

Both build commands exited with status `0`. Both guests reached the serial shell and reported `active` for `multi-user.target`. Each ISO was 1,498,152,960 bytes.

```bash
./build-iso.sh
sha256sum result/iso/*.iso
qemu-system-x86_64 -enable-kvm -smp 2 -m 2048 -nic none -cdrom result/iso/*.iso -nographic
```

In the guest, run `hostname`, `cat /etc/nexos-release`, `uname -r`, `nixos-version` and `systemctl is-active multi-user.target`. Change the hostname in `nexos.nix` and repeat the build and boot to check that the new value appears in the next guest.

P00 implementation and independent qualification remain pending.
