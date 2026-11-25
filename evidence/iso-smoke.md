# Live ISO smoke test

## Klassy and Opal Fruits

Built the Plasma ISO from the Nix configuration at commit `4baaee6bb8b8470693c925d65ff2170a4e26f9a4` on 2026-11-25 with Klassy `6.5.3`. The ISO SHA-256 is `e5c518358d78516bf554826182ab7b811d4e1b95f4eaa4dcad1f699367f34ddb`.

A fresh live session under QEMU/KVM selected Klassy Kite Light with the bottom panel. KWin read `org.kde.klassy`, the Opal Fruits button placement `MFS` and `HAI_X`, `StyleSuessigKite` and a corner radius of `5`. The session used the regenerated Klassy icons. KWin mapped `org.kde.klassy.so` and a Konsole window mapped `klassy6.so` during the test. The installation copy of `plasma.nix` matched the tested source byte for byte.

The first boot with only system-wide window defaults selected Breeze because Plasma initialized the session from its global theme. Selecting Klassy as the global theme resolved that priority conflict. The guest shut down at the end of the successful test.

## Console and Plasma editions

Built on 2026-11-25 from the Nix configuration at commit `c5ddf1cac31c4ee09affe82edee6db9aa1c16dff`. Both builds used Nixpkgs `0dc498bfe49baeb18b0f9891e800b53bb2603193`. The console build ran from a clean clone, and the Plasma derivation matched the derivation evaluated from that clone.

| Edition | Bytes | SHA-256 |
| --- | ---: | --- |
| Console | 1,538,981,888 | `c0cbc49db936d094bd995f0d9507e99d8342a15e95c0d072a9b8494dad014d55` |
| Plasma | 3,613,261,824 | `df979f6f93c37ef2a0c6a22e8df8a5b055b6a1cf50f3b4ddec53d87fac9ddcb2` |

Both ISOs booted under QEMU `8.2.2` with KVM, BIOS and no network or persistent disk, and both returned `git version 2.54.0`. The console guest had neither `kwin_wayland` nor `plasmashell`. The Plasma guest used virtio VGA and reported `active` for both `plasma-kwin_wayland.service` and `plasma-plasmashell.service`.

Both live images exposed `/etc/nexos/install/edition.nix`. The console file imported `./nexos.nix`. The Plasma file imported `./nexos.nix` and `./plasma.nix`. Both editions installed successfully to fresh virtual disks and booted without the ISO. Git 2.54.0 was available in both installed systems. The Plasma services were active on the Plasma installation, and the console installation lacked both desktop executables.

The disk tests used the [README recipe](../README.md#install-an-edition-to-disk), ext4, BIOS GRUB and a test user. The initial console install hit a disabled flakes feature when `nixos-install` used the default Nixpkgs lookup. Passing the bundled channel explicitly with `-I` resolved the error and was used for both successful installs.

## Original single-edition image

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
