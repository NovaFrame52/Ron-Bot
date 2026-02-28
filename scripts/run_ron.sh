#!/usr/bin/env bash
set -euo pipefail

# One-click runner for Ron Bot
# Usage: ./run_ron.sh [-f|--force] [-v|--verbose]
# Creates a virtualenv (./.venv), installs requirements, loads .env, and runs the bot.

# Parse args
FORCE=0
VERBOSE=0
while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force) FORCE=1; shift ;;
    -v|--verbose) VERBOSE=1; shift ;;
    -h|--help) echo "Usage: $0 [-f|--force] [-v|--verbose]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# Resolve script/project root so the script works regardless of CWD or when invoked via symlink
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Ensure python3 is available
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found; please install Python 3." >&2
  exit 1
fi

# Create venv if missing (in project root)
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
  if [ "$VERBOSE" -eq 1 ]; then
    echo "Creating virtualenv..."
  fi
  python3 -m venv "$PROJECT_ROOT/.venv"
fi

# Activate venv
# shellcheck disable=SC1091
. "$PROJECT_ROOT/.venv/bin/activate"

# Bootstrap pip if not available, then upgrade and install deps
python3 -m ensurepip --upgrade 2>/dev/null || true
if [ "$VERBOSE" -eq 1 ]; then
  pip install --upgrade pip
  pip install -r "$PROJECT_ROOT/requirements.txt"
else
  pip install --upgrade pip >/dev/null 2>&1
  pip install -r "$PROJECT_ROOT/requirements.txt" >/dev/null 2>&1
fi

# Load env vars from .env (if present) in project root and secure it
if [ -f "$PROJECT_ROOT/.env" ]; then
  if [ "$VERBOSE" -eq 1 ]; then
    echo "Found .env — checking permissions and loading environment..."
  fi

  # Only set restrictive permissions if they're not already 600
  current_perm="$(stat -c %a "$PROJECT_ROOT/.env" 2>/dev/null || echo "")"
  if [ "$current_perm" != "600" ]; then
    if [ "$VERBOSE" -eq 1 ]; then
      echo "Setting restrictive permissions on .env..."
    fi
    chmod 600 "$PROJECT_ROOT/.env" || true
  fi

  # Temporarily load env variables (don't print secrets)
  set -a
  # shellcheck disable=SC1091
  . "$PROJECT_ROOT/.env"
  set +a

  # Basic validation for DISCORD_TOKEN
  if [ -z "${DISCORD_TOKEN:-}" ]; then
    echo "Error: DISCORD_TOKEN not set in .env. Add your token or export DISCORD_TOKEN before running." >&2
    exit 1
  fi

  # Catch common placeholder value
  if [ "${DISCORD_TOKEN}" = "your_token_here" ]; then
    echo "Error: DISCORD_TOKEN in .env looks like the placeholder value. Please replace it with your real token." >&2
    exit 1
  fi

  # Basic malformed-token check (tokens usually contain dots)
  if [[ "${DISCORD_TOKEN}" != *.*.* ]]; then
    if [ "$FORCE" -eq 1 ]; then
      if [ "$VERBOSE" -eq 1 ]; then
        echo "Warning: DISCORD_TOKEN looks malformed, but --force provided; continuing."
      fi
    else
      echo "Warning: DISCORD_TOKEN looks malformed. Continue anyway? (y/N)"
      read -r answer
      case "$answer" in
        [Yy]|[Yy][Ee][Ss]) ;;
        *) echo "Aborting."; exit 1 ;;
      esac
    fi
  fi
else
  if [ -z "${DISCORD_TOKEN:-}" ]; then
    echo "Error: DISCORD_TOKEN not set in .env or environment." >&2
    exit 1
  fi
fi


# Prevent double-start
PIDFILE="$PROJECT_ROOT/ron.pid"
if [ -f "$PIDFILE" ]; then
  PID_EXIST="$(cat "$PIDFILE" 2>/dev/null || true)"
  if kill -0 "$PID_EXIST" >/dev/null 2>&1; then
    echo "Ron appears to be already running (PID $PID_EXIST)." >&2
    exit 1
  else
    rm -f "$PIDFILE"
  fi
fi

if [ "$VERBOSE" -eq 1 ]; then
  echo "Starting Ron Bot..."
fi

# Start in background and save PID.  Use the venv's python executable to
# avoid cases where the shell's PATH isn't modified correctly (see issues
# where the bot throws ModuleNotFoundError for dotenv).
PYTHON_EXEC="$PROJECT_ROOT/.venv/bin/python"
if [ ! -x "$PYTHON_EXEC" ]; then
  # fallback to plain python3; the activate step above *should* have ensured
  # pip installed packages are available, but be explicit here so the error
  # message later is more predictable.
  PYTHON_EXEC="python3"
fi

nohup "$PYTHON_EXEC" "$PROJECT_ROOT/ron_bot.py" >>"$PROJECT_ROOT/ron.log" 2>&1 &
echo $! >"$PIDFILE"
PID_VAL="$(cat "$PIDFILE" 2>/dev/null || true)"
echo "Started Ron (PID ${PID_VAL}). Logs: $PROJECT_ROOT/ron.log"

