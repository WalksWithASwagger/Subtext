#!/bin/sh
# macOS/Linux counterpart to start.bat: run the server (from .venv if there is
# one) and open the browser once it answers. The poller gives up when the
# server exits: $$ is this script's PID, which exec hands to python.
cd "$(dirname "$0")" || exit 1
PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python
echo "Starting Subtext ... (model + lens take ~1 min to load)"
(
  until curl -sf -o /dev/null http://127.0.0.1:8765/; do
    kill -0 $$ 2>/dev/null || exit 0
    sleep 1
  done
  open http://localhost:8765 2>/dev/null || xdg-open http://localhost:8765 2>/dev/null
) &
exec "$PY" -u server.py
