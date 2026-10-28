#!/usr/bin/env python3
"""Run a playback visualizer for the lifetime of this Hyprlock instance."""
import fcntl
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time


def render_frame(raw):
    try:
        values = [int(v) for v in raw.strip().split(b";") if v]
    except ValueError:
        return ""
    if len(values) != 20 or not any(values):
        return ""
    return '<span letter_spacing="2048">' + "".join(
        "\u2007▁▂▃▄▅▆▇█"[max(0, min(8, v))] for v in values
    ) + "</span>"


def main():
    runtime = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")) / "hyprlock-cava"
    runtime.mkdir(mode=0o700, exist_ok=True)
    guard = (runtime / "lock").open("w")
    try:
        fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return 0
    frame = runtime / "frame"
    previous = None

    def publish(text):
        nonlocal previous
        if text == previous:
            return
        tmp = runtime / "frame.tmp"
        tmp.write_text(text + "\n")
        tmp.replace(frame)
        previous = text

    def interrupted(signum, _frame):
        raise SystemExit(128 + signum)

    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, interrupted)
    cava = None
    publish("")
    try:
        # Start the locker even if Cava is missing or fails.
        locker = subprocess.Popen(["hyprlock", *sys.argv[1:]])
        config = Path(__file__).resolve().parent.parent / "hyprlock-cava.conf"
        with (runtime / "cava.log").open("w") as log:
            try:
                cava = subprocess.Popen(["cava", "-p", str(config)], stdout=subprocess.PIPE, stderr=log)
            except OSError:
                return locker.wait()
            with selectors.DefaultSelector() as selector:
                selector.register(cava.stdout, selectors.EVENT_READ)
                pending = b""
                last_frame = time.monotonic()
                while locker.poll() is None:
                    for key, _ in selector.select(timeout=0.2):
                        chunk = os.read(key.fd, 4096)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            publish("")
                            continue
                        pending += chunk
                        if b"\n" in pending:
                            # Display only the newest complete frame if reads arrive in a batch.
                            complete, pending = pending.rsplit(b"\n", 1)
                            raw = complete.rsplit(b"\n", 1)[-1]
                            publish(render_frame(raw))
                            last_frame = time.monotonic()
                    if time.monotonic() - last_frame > 1:
                        publish("")
        return locker.returncode
    finally:
        if cava is not None:
            if cava.poll() is None:
                cava.terminate()
                try:
                    cava.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    cava.kill()
                    cava.wait()
            cava.stdout.close()
        publish("")
        guard.close()
        # Never terminate the locker as part of visualizer cleanup.


if __name__ == "__main__":
    sys.exit(main())
