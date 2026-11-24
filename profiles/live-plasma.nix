{
  imports = [ ./plasma.nix ];

  services.displayManager.autoLogin = {
    enable = true;
    user = "nixos";
  };

  environment.etc."nexos/install/plasma.nix".source = ./plasma.nix;
}
