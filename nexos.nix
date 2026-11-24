{ config, lib, pkgs, ... }:

{
  networking.hostName = lib.mkDefault "nexos";

  environment.systemPackages = [
    pkgs.git
  ];

  boot.zfs.forceImportRoot = false;

  environment.etc."nexos-release".text = ''
    NAME=NexOS
    HOSTNAME=${config.networking.hostName}
  '';
}
