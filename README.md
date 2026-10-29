# Kelpos Hyprlock — laptop

This `laptop` branch preserves the laptop lock screen. The desktop version remains on `main`; keep laptop updates on this branch.

It includes the laptop's larger clock/avatar layout, translucent username and password fields, coloured authentication feedback, song artwork, media controls and 20-bar Cava visualizer. Failed authentication briefly flashes the password border red, returning to neutral after 900 ms.

## Install

```sh
git clone --branch laptop https://github.com/Otamarau/kelpos-hyprlock-theme.git
cd kelpos-hyprlock-theme
backup="$HOME/.local/state/theme-backups/hyprlock-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup" ~/.config/hypr/assets
cp -a ~/.config/hypr/. "$backup/"
cp hyprlock.conf hyprlock-cava.conf ~/.config/hypr/
install -m 755 albumart.sh songdetail.sh mediactl.sh lock-with-cava.py ~/.config/hypr/
cp assets/laptop-wallpaper.jpg assets/laptop-avatar.jpg ~/.config/hypr/assets/
```

The published config points to the bundled images under `~/.config/hypr/assets/` instead of machine-specific image paths. Helpers are installed directly in `~/.config/hypr/`, matching the laptop Waybar power menu. Unlike the desktop branch, they are not under `Scripts/`.

To lock with media and Cava:

```sh
~/.config/hypr/albumart.sh >/dev/null 2>&1
/usr/bin/python3 ~/.config/hypr/lock-with-cava.py
```

This locks the screen; use your normal system password to unlock. Direct `hyprlock` launches omit the Cava helper. Configuration changes apply on the next lock.

## Dependencies and checks

The laptop uses Hyprlock 0.9.6, Python 3, Bash, JetBrainsMono Nerd Font, Playerctl, curl, Cava and a PulseAudio/PipeWire-Pulse source. A Wayland session with `XDG_RUNTIME_DIR` is required. If Cava fails, the wrapper still runs the locker and never terminates it during visualizer cleanup.

Artwork caches live under `~/.cache/hyprlock`; visualizer state is in `$XDG_RUNTIME_DIR/hyprlock-cava`. No runtime caches, logs or authentication data are included. The bundled wallpaper/avatar are the same image assets already present in the desktop repository.

```sh
/usr/bin/python3 -m unittest discover -s tests -v
for script in *.sh; do bash -n "$script"; done
```

Tests simulate visualizer frames without locking the desktop. Live authentication and layout should be checked in your session.

Copy future live changes back into this checkout, retaining the portable asset paths, and push to `laptop`, not `main`.
