# Kelpos Hyprlock Theme

A personal Hyprlock configuration with a blurred wallpaper, circular profile image, large clock, rounded password field and media visualizer.

## Features

- Shared JetBrainsMono Nerd Font typography and a centred date, clock and username.
- Blurred wallpaper and circular profile image, both included under `assets/`.
- Translucent password field with brief failure-border feedback and a Caps Lock indicator.
- Current song, album artwork and clickable previous/play-pause/next controls.
- A 20-bar Cava visualizer that runs alongside the lock screen.

## Requirements

- Hyprlock (the source configuration was developed with version 0.9.6).
- JetBrainsMono Nerd Font.
- Python 3 and Bash.
- Playerctl and an MPRIS-capable player for media information and controls.
- Cava with PulseAudio input, using PulseAudio or PipeWire's PulseAudio compatibility service.
- curl for downloading remote album artwork.
- A Wayland desktop session with `XDG_RUNTIME_DIR` set.

The visualizer uses the Python standard library. If Cava cannot start, the wrapper still starts Hyprlock. Visualizer cleanup does not terminate the locker.

## Installation

Keep a backup of your current `~/.config/hypr/hyprlock.conf` and any matching scripts before copying these files. From the repository directory:

```sh
mkdir -p ~/.config/hypr/Scripts ~/.config/hypr/assets
cp hyprlock.conf hyprlock-cava.conf ~/.config/hypr/
install -m 755 Scripts/albumart.sh Scripts/songdetail.sh Scripts/mediactl.sh Scripts/lock-with-cava.py ~/.config/hypr/Scripts/
cp assets/wallpaper.jpg assets/avatar.jpg ~/.config/hypr/assets/
```

This installs only the lock-screen files; it does not replace your main Hyprland configuration. The repository is separate from the installed files: copy later live edits back into the repo before committing them.

### Launch with media and the visualizer

```sh
~/.config/hypr/Scripts/albumart.sh >/dev/null 2>&1
~/.config/hypr/Scripts/lock-with-cava.py
```

This locks the screen. Use your normal system password to unlock it. For Hyprland configurations using the traditional binding syntax:

```ini
bind = SUPER, L, exec, ~/.config/hypr/Scripts/albumart.sh >/dev/null 2>&1; ~/.config/hypr/Scripts/lock-with-cava.py
```

The corresponding binding in the source desktop's Lua configuration is:

```lua
hl.bind("SUPER + L", hl.dsp.exec_cmd("~/.config/hypr/Scripts/albumart.sh >/dev/null 2>&1; ~/.config/hypr/Scripts/lock-with-cava.py"))
```

Use the syntax supported by your installed Hyprland version. Launching `hyprlock` directly displays the layout but does not start the Cava helper.

## Customization

- Replace `assets/wallpaper.jpg` and `assets/avatar.jpg`, then copy them to `~/.config/hypr/assets/`.
- Edit `$lock_font` at the top of `hyprlock.conf` to change the shared font.
- The empty `monitor` fields apply widgets to all monitors. Positions are tuned to the original desktop and may need adjusting for different resolutions.
- Edit `hyprlock-cava.conf` for visualizer sensitivity and audio input. Its 20-bar output matches the Python renderer; change both together if changing the bar count.
- Media scripts prefer a playing player, then a paused player. Artwork is downloaded only when needed and cached under `~/.cache/hyprlock` by default.
- Visualizer state and logs live under `$XDG_RUNTIME_DIR/hyprlock-cava`, outside the repository.
- The configuration uses `~/.cache/hyprlock/album-art` as its initial artwork path. If you use a custom `XDG_CACHE_HOME`, adjust that path as well.

## Files

| Path | Purpose |
| --- | --- |
| `hyprlock.conf` | Lock-screen layout, password field and media widgets |
| `hyprlock-cava.conf` | Audio capture and raw visualizer output |
| `Scripts/lock-with-cava.py` | Starts Hyprlock and manages the visualizer's lifetime |
| `Scripts/albumart.sh` | Resolves/caches album artwork |
| `Scripts/songdetail.sh` | Escapes media metadata for Pango labels |
| `Scripts/mediactl.sh` | Playback actions and play/pause indicator |
| `assets/` | Wallpaper and avatar from the original setup |

The images are included as supplied with this personal setup; no separate image authorship or licensing claim is made here.

## Checks

```sh
python3 -m unittest discover -s tests -v
for script in Scripts/*.sh; do bash -n "$script"; done
```

These checks exercise frame rendering without starting Hyprlock or locking the desktop. Runtime compatibility still needs checking in your own Wayland session.
