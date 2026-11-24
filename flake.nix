{
  description = "NexOS live image for the reference VM";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
    in
    {
      nixosConfigurations.nexos = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [ ./nexos.nix ];
      };

      packages.${system}.iso = self.nixosConfigurations.nexos.config.system.build.isoImage;
    };
}
