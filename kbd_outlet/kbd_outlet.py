#!/usr/bin/env python3
"""
kbd-outlet: Grab a specific keyboard exclusively, remap its keys to
custom (verified-unused) keycodes, and emit them via a uinput virtual
device. Hyprland sees the virtual device normally; the grabbed physical
keyboard disappears from the OS entirely.

Usage:
    python kbd_outlet.py --device /dev/input/by-id/usb-...-event-kbd --config keymap.json

SAFETY NOTES (read before first run):
  * The grab is EXCLUSIVE. If you point --device at your ONLY keyboard,
    you can lock yourself out: Ctrl+C may not reach the terminal and
    Ctrl+Alt+F2 may not switch TTYs, because the compositor never sees
    those keys. For the first run, do ONE of:
        - run it over SSH from another machine, or
        - keep a second, un-grabbed keyboard plugged in, or
        - use --timeout 30 so it auto-releases after 30s no matter what.
  * Prefer a stable path under /dev/input/by-id/ over /dev/input/eventN
    (the eventN numbers shuffle across reboots/replugs).
"""

import argparse
import json
import logging
import select
import signal
import sys
import time
from pathlib import Path

import evdev
from evdev import UInput, ecodes as e

KEY_MAX = 0x2ff  # 767 — kernel KEY_MAX; output codes must be in 1..KEY_MAX

# ---------------------------------------------------------------------------
# Minimal DEMO map (used only when --config is omitted). It maps three keys
# to verified-UNASSIGNED codes so it follows the same "no real-hardware
# collision" rule as the shipped keymap.json. For real use, pass --config.
# ---------------------------------------------------------------------------
DEFAULT_MAP: dict[int, int] = {
    e.KEY_Q: 195,
    e.KEY_W: 196,
    e.KEY_E: 197,
}


def resolve_code(name: str) -> int | None:
    """Resolve 'KEY_F13' (ecodes constant) or 'code:195' (raw int) to an int."""
    if isinstance(name, int):
        return name
    if name.startswith("code:"):
        try:
            return int(name.split(":", 1)[1])
        except ValueError:
            return None
    val = getattr(e, name, None)
    return val if isinstance(val, int) else None


def valid_out(code: int | None) -> bool:
    return code is not None and 0 < code <= KEY_MAX


def load_config(path: str) -> dict[int, int]:
    """Load a JSON keymap, converting names / code:N to ints, with validation."""
    raw = json.loads(Path(path).read_text())
    result: dict[int, int] = {}
    for src_name, dst_name in raw.items():
        if isinstance(src_name, str) and src_name.startswith("_"):
            continue  # comment key
        src = resolve_code(src_name)
        dst = resolve_code(dst_name)
        if src is None:
            logging.warning("Unknown source keycode %r — skipped", src_name)
            continue
        if not valid_out(dst):
            logging.warning("Dest %r for %s is invalid or > KEY_MAX (%d) — skipped",
                            dst_name, src_name, KEY_MAX)
            continue
        if dst in result.values():
            logging.warning("Dest code %d is used more than once — last one wins", dst)
        result[src] = dst
    return result


def build_uinput(keymap: dict[int, int], passthrough_caps: set[int] | None) -> UInput:
    """Virtual keyboard advertising exactly the codes we may emit."""
    out_codes = set(keymap.values())
    if passthrough_caps:
        out_codes |= passthrough_caps
    out_codes = {c for c in out_codes if valid_out(c)}
    caps = {e.EV_KEY: sorted(out_codes)}
    return UInput(caps, name="kbd-outlet-virtual", version=0x1)


def open_device(device_path: str) -> evdev.InputDevice:
    try:
        return evdev.InputDevice(device_path)
    except FileNotFoundError:
        logging.error("No such device: %s", device_path)
    except PermissionError:
        logging.error("Permission denied opening %s.", device_path)
        logging.error("Add yourself to the 'input' group (then re-login), or run with sudo.")
    sys.exit(1)


def run(device_path: str, keymap: dict[int, int], *,
        timeout: float, passthrough: bool, grab_delay: float) -> None:
    dev = open_device(device_path)
    logging.info("Target device: %s  (%s)", dev.name, device_path)

    if grab_delay > 0:
        logging.warning("Grabbing EXCLUSIVELY in %.0fs — press Ctrl+C now if this is the wrong device.",
                        grab_delay)
        try:
            time.sleep(grab_delay)
        except KeyboardInterrupt:
            logging.info("Aborted before grab. Nothing was changed.")
            sys.exit(0)

    pass_caps = None
    if passthrough:
        # advertise the source keyboard's own keys too, so unmapped keys pass through
        pass_caps = set(dev.capabilities().get(e.EV_KEY, []))

    try:
        dev.grab()  # EXCLUSIVE: OS + all other processes are now blind to this device
    except OSError as err:
        logging.error("Could not grab %s: %s", device_path, err)
        dev.close()
        sys.exit(1)

    ui = build_uinput(keymap, pass_caps)
    logging.info("Virtual device created: %s", ui.device.path)
    time.sleep(0.3)  # let libinput/Hyprland register the new device before events flow

    released = {"done": False}

    def cleanup(signum=None, frame=None):
        if released["done"]:
            return
        released["done"] = True
        logging.info("Releasing keyboard and shutting down...")
        try:
            dev.ungrab()
        except Exception:
            pass
        try:
            dev.close()
        finally:
            ui.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    if timeout > 0:
        logging.info("Failsafe: will auto-release after %.0fs.", timeout)
    logging.info("Listening. Press Ctrl+C to stop.")

    start = time.monotonic()
    while True:
        if timeout > 0 and (time.monotonic() - start) >= timeout:
            logging.info("Timeout reached.")
            cleanup()
        # wake at least once a second so the timeout check stays responsive
        r, _, _ = select.select([dev.fd], [], [], 1.0)
        if not r:
            continue
        try:
            events = list(dev.read())
        except OSError:
            logging.error("Device read failed (unplugged?). Releasing.")
            cleanup()
        for event in events:
            if event.type != e.EV_KEY:
                continue
            src_code = event.code
            value = event.value  # 0=up, 1=down, 2=repeat

            if src_code in keymap:
                dst = keymap[src_code]
                logging.debug("%s -> code:%d (value=%d)",
                              e.KEY.get(src_code, src_code), dst, value)
                ui.write(e.EV_KEY, dst, value)
                ui.syn()
            elif passthrough:
                ui.write(e.EV_KEY, src_code, value)
                ui.syn()
            else:
                logging.debug("Swallowed unmapped key %s value=%d",
                              e.KEY.get(src_code, src_code), value)


def main():
    p = argparse.ArgumentParser(description="kbd-outlet: remap a keyboard to custom keycodes")
    p.add_argument("--device", required=True,
                   help="Input device path, ideally /dev/input/by-id/...-event-kbd")
    p.add_argument("--config", help="JSON keymap file (overrides the built-in demo map)")
    p.add_argument("--timeout", type=float, default=0.0,
                   help="Auto-release after N seconds (0 = never). Use this for first runs.")
    p.add_argument("--passthrough", action="store_true",
                   help="Forward UNmapped keys unchanged instead of swallowing them (safer for testing)")
    p.add_argument("--grab-delay", type=float, default=3.0,
                   help="Seconds to wait before grabbing, so you can abort (default 3)")
    p.add_argument("--list-keys", action="store_true", help="Print all KEY_ names and exit")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    if args.list_keys:
        for name, code in sorted(e.KEY.items(), key=lambda x: x[1] if isinstance(x[1], int) else 0):
            print(f"{str(name):30s} = {code}")
        sys.exit(0)

    if args.config:
        keymap = load_config(args.config)
    else:
        logging.warning("No --config given; using the 3-key built-in DEMO map. "
                        "Pass --config keymap.json for the full layout.")
        keymap = dict(DEFAULT_MAP)

    if not keymap:
        logging.error("Keymap is empty after validation — nothing to do.")
        sys.exit(1)
    logging.info("Loaded %d key mappings.", len(keymap))

    run(args.device, keymap,
        timeout=args.timeout, passthrough=args.passthrough, grab_delay=args.grab_delay)


if __name__ == "__main__":
    main()
