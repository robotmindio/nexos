{ lib, pkgs, ... }:

let
  opalFruits = pkgs.runCommand "klassy-opal-fruits-defaults" { } ''
    export HOME="$TMPDIR"
    export XDG_CONFIG_HOME="$TMPDIR/config"
    export XDG_CONFIG_DIRS="$TMPDIR/config-defaults"
    export XDG_DATA_HOME="$TMPDIR/data"
    export XDG_DATA_DIRS=${pkgs.klassy}/share
    export QT_QPA_PLATFORM=offscreen

    ${pkgs.klassy}/bin/klassy-settings --load-windeco-preset 'Opal Fruits'
    ${pkgs.kdePackages.kconfig}/bin/kwriteconfig6 --file "$XDG_CONFIG_HOME/kwinrc" \
      --group org.kde.kdecoration2 --key library org.kde.klassy

    install -Dm644 "$XDG_CONFIG_HOME/kwinrc" "$out/kwinrc"
    install -Dm644 "$XDG_CONFIG_HOME/klassy/klassyrc" "$out/klassy/klassyrc"
    mkdir -p "$out/share"
    cp -r "$XDG_DATA_HOME/icons" "$out/share/"
  '';
in
{
  hardware.graphics.enable = true;
  services.desktopManager.plasma6.enable = true;
  services.displayManager.plasma-login-manager.enable = true;

  environment.systemPackages = [ pkgs.klassy (lib.hiPrio opalFruits) ];

  environment.etc = {
    "xdg/kwinrc".source = "${opalFruits}/kwinrc";
    "xdg/klassy/klassyrc".source = "${opalFruits}/klassy/klassyrc";
    "xdg/kdeglobals".text = ''
      [KDE]
      LookAndFeelPackage=org.kde.klassykitelightbottompanel.desktop
      widgetStyle=Klassy
    '';
  };
}
