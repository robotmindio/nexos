{ config, lib, ... }:

{
  imports = [ ../nexos.nix ];

  boot.kernelParams = [
    "console=tty0"
    "console=ttyS0,115200n8"
  ];

  isoImage.edition = if config.services.desktopManager.plasma6.enable then "nexos-plasma" else "nexos-console";
  isoImage.squashfsCompression = "zstd -Xcompression-level 6";

  environment.etc."nexos/install/nexos.nix".source = ../nexos.nix;
  environment.etc."nexos/install/edition.nix".text = ''
    {
      imports = [ ./nexos.nix ${lib.optionalString config.services.desktopManager.plasma6.enable "./plasma.nix"} ];
    }
  '';
}
