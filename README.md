# KBD_OUTLET
A lightweight python daemon for hyprland to make a macro keyboard
I recommend saving to ~/.local/share/kbd-outlet since thats the default for launching the keybind.conf
This project was originally made specifically for a redragon k630, which is a 60% keyboard, so some keys may not be mapped. 

# kbd-outlet

A lightweight, event-driven Linux daemon to transform a secondary keyboard into a dedicated macro matrix.

## Overview
Grab a specific keyboard exclusively, remap its keys to custom (verified-unused) keycodes, and emit them via a `uinput` virtual device. Hyprland sees the virtual device normally; the grabbed physical keyboard disappears from the OS entirely.

## Usage
```bash
python kbd_outlet.py --device /dev/input/by-id/usb-...-event-kbd --config keymap.json
```

## Safety Notes (Read before first run)
* **The grab is EXCLUSIVE.** If you point `--device` at your ONLY keyboard, you can lock yourself out: `Ctrl+C` may not reach the terminal and `Ctrl+Alt+F2` may not switch TTYs, because the compositor never sees those keys. For the first run, do ONE of:
  * Run it over SSH from another machine, or
  * Keep a second, un-grabbed keyboard plugged in, or
  * Use `--timeout 30` so it auto-releases after 30s no matter what.
* Prefer a stable path under `/dev/input/by-id/` over `/dev/input/eventN` (the `eventN` numbers shuffle across reboots/replugs).

## Integration with Hyprland
**NO MATH REQUIRED.** Each code is ALREADY the Hyprland keycode (the physical key's evdev code + 8, the xkb offset). 

Every code maps to a verified-UNASSIGNED kernel keycode: no real keyboard, laptop, or multimedia device emits these, so nothing can conflict.

Verify a key with `wev` (press it, read the 'code' it reports).
