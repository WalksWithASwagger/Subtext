#!/bin/sh
# macOS/Linux counterpart to start.bat: run the server (from .venv if there is
# one) and open the browser once it answers.
cd "$(dirname "$0")" || exit 1
PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python
echo "Starting Subtext ... (model + lens take ~1 min to load)"
(
  n=0
  until curl -sf -o /dev/null http://127.0.0.1:8765/ || [ $n -ge 600 ]; do sleep 1; n=$((n + 1)); done
  [ $n -lt 600 ] && { open http://localhost:8765 2>/dev/null || xdg-open http://localhost:8765 2>/dev/null; }
) &
exec "$PY" -u server.py
