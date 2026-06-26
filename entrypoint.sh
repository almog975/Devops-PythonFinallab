#!/bin/bash
set -e

# ── Step 4a: Move dummy data from temp location → mounted volume ──────────────
# Only copy if the volume is empty (don't overwrite live data on restarts)
if [ ! -f /data/lab_data.json ]; then
    echo "[entrypoint] Initializing volume with dummy data..."
    cp /tmp/lab_data.json /data/lab_data.json
    echo "[entrypoint] Data written to /data/lab_data.json"
else
    echo "[entrypoint] Volume already has data, skipping init."
fi

# ── Step 4b: Erase dummy data from temp location ─────────────────────────────
rm -f /tmp/lab_data.json
echo "[entrypoint] Temp data cleared."

# ── Step 4c: Start nginx in foreground ───────────────────────────────────────
echo "[entrypoint] Starting nginx..."
exec nginx -g "daemon off;"
