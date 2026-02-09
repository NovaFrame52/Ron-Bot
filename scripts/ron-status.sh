#!/usr/bin/env bash
set -euo pipefail

# Show Ron Bot status
# Usage: ron-status.sh [-t|--tail N] [-v|--verbose]

TAIL=0
VERBOSE=0
while [ $# -gt 0 ]; do
  case "$1" in
    -t|--tail)
      TAIL=${2:-0}
      shift 2 || true
      ;;
    -v|--verbose) VERBOSE=1; shift ;;
    -h|--help) echo "Usage: $0 [-t|--tail N] [-v|--verbose]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Resolve script/project root
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check for systemd service
if command -v systemctl >/dev/null 2>&1; then
  SERVICE_STATUS=$(systemctl --user is-active ron.service 2>/dev/null || echo "inactive")
  echo "Systemd Service (ron.service): $SERVICE_STATUS"
  if [ "$SERVICE_STATUS" = "active" ]; then
    systemctl --user status ron.service --no-pager 2>/dev/null | head -20 || true
  fi
fi

# Check running processes
PIDS=$(pgrep -f "ron_bot.py" || true)
if [ -z "$PIDS" ]; then
  echo "Ron Bot process: Not running"
else
  echo "Ron Bot process: Running (PIDs): $PIDS"
  for pid in $PIDS; do
    ps -o pid,cmd,etime -p "$pid" 2>/dev/null || true
  done
fi

# Check PID file from run_ron.sh
PIDFILE="$PROJECT_ROOT/ron.pid"
if [ -f "$PIDFILE" ]; then
  PID_VAL="$(cat "$PIDFILE" 2>/dev/null || true)"
  echo "PID file: $PIDFILE (PID: $PID_VAL)"
  if ! kill -0 "$PID_VAL" 2>/dev/null; then
    echo "  (PID not running; file may be stale)"
  fi
else
  echo "PID file: Not found"
fi

# Config status
if [ -f "$PROJECT_ROOT/.env" ]; then
  echo "Configuration: .env found"
  if grep -q "your_token_here" "$PROJECT_ROOT/.env" 2>/dev/null; then
    echo "  ⚠ DISCORD_TOKEN still has placeholder value"
  fi
else
  echo "Configuration: .env not found"
fi

exit 0
