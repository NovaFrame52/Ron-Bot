#!/usr/bin/env bash
set -euo pipefail

# Stop Ron Bot
# Usage: stop_ron.sh [-f|--force]
# Use -f/--force to avoid interactive prompts

FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force) FORCE=1; shift ;;
    -h|--help) echo "Usage: $0 [-f|--force]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PIDFILE="$PROJECT_ROOT/ron.pid"

# Try both methods: PID file and process search
PIDS=""

# Check PID file if present
if [ -f "$PIDFILE" ]; then
  PID_FROM_FILE="$(cat "$PIDFILE" 2>/dev/null || true)"
  if [ -n "$PID_FROM_FILE" ] && kill -0 "$PID_FROM_FILE" >/dev/null 2>&1; then
    PIDS="$PID_FROM_FILE"
  fi
fi

# Also search for running processes
PIDS_FROM_PS=$(pgrep -f "ron_bot.py" || true)
if [ -n "$PIDS_FROM_PS" ]; then
  PIDS="$PIDS_FROM_PS"
fi

if [ -z "$PIDS" ]; then
  if [ -f "$PIDFILE" ]; then
    rm -f "$PIDFILE"
  fi
  echo "No Ron Bot process found."
  exit 0
fi

echo "Found Ron Bot PIDs: $PIDS"

if [ "$FORCE" -eq 0 ]; then
  read -r -p "Send SIGTERM to stop them gracefully? (y/N) " answer
  case "$answer" in
    [Yy]|[Yy][Ee][Ss]) ;;
    *) echo "Aborting."; exit 1 ;;
  esac
else
  echo "--force provided; proceeding without prompt."
fi

# Send SIGTERM
for pid in $PIDS; do
  if kill -0 "$pid" >/dev/null 2>&1; then
    echo "Sending SIGTERM to $pid..."
    kill -TERM "$pid" || true
  fi
done

# Wait for processes to exit (up to 10s)
timeout=10
elapsed=0
while [ $elapsed -lt $timeout ]; do
  sleep 1
  elapsed=$((elapsed+1))
  STILL=$(pgrep -f "ron_bot.py" || true)
  if [ -z "$STILL" ]; then
    if [ -f "$PIDFILE" ]; then
      rm -f "$PIDFILE"
    fi
    echo "Processes stopped."
    exit 0
  fi
done

# Force kill if still running
STILL=$(pgrep -f "ron_bot.py" || true)
if [ -n "$STILL" ]; then
  echo "Processes still running after $timeout seconds: $STILL"
  if [ "$FORCE" -eq 0 ]; then
    read -r -p "Send SIGKILL to force kill? (y/N) " answer
    case "$answer" in
      [Yy]|[Yy][Ee][Ss]) ;;
      *) echo "Aborting."; exit 1 ;;
    esac
  else
    echo "--force provided; sending SIGKILL."
  fi
  for pid in $STILL; do
    if kill -0 "$pid" >/dev/null 2>&1; then
      echo "Force killing $pid..."
      kill -KILL "$pid" || true
    fi
  done
  if [ -f "$PIDFILE" ]; then
    rm -f "$PIDFILE"
  fi
fi

echo "Done."
exit 0