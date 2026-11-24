{ config, modulesPath, ... }:

{
  imports = [ "${modulesPath}/installer/cd-dvd/installation-cd-minimal.nix" ];

  networking.hostName = "nexos";

  boot.kernelParams = [
    "console=tty0"
    "console=ttyS0,115200n8"
  ];
  boot.zfs.forceImportRoot = false;

  environment.etc."nexos-release".text = ''
    NAME=NexOS
    HOSTNAME=${config.networking.hostName}
  '';
}
