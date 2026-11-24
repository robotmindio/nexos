{
  description = "NexOS console and Plasma live images";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      installer = "${nixpkgs}/nixos/modules/installer/cd-dvd";
      console = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [ "${installer}/installation-cd-minimal.nix" ./profiles/live-iso.nix ];
      };
      plasma = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          "${installer}/installation-cd-base.nix"
          ./profiles/live-iso.nix
          ./profiles/live-plasma.nix
        ];
      };
    in
    {
      nixosConfigurations = {
        nexos = console;
        nexos-console = console;
        nexos-plasma = plasma;
      };

      packages.${system} = {
        iso = self.packages.${system}.iso-console;
        iso-console = console.config.system.build.isoImage;
        iso-plasma = plasma.config.system.build.isoImage;
      };
    };
}
