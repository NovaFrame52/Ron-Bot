#!/usr/bin/env bash
set -euo pipefail

# Uninstaller for Ron Bot
# Usage: ./uninstall_all.sh [-f|--force] [--remove-venv]
# -f, --force: non-interactive (assume yes)
# --remove-venv: delete the .venv directory

FORCE=0
REMOVE_VENV=0

while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force) FORCE=1; shift ;;
    --remove-venv) REMOVE_VENV=1; shift ;;
    -h|--help) echo "Usage: $0 [-f|--force] [--remove-venv]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

echo "Starting Ron Bot uninstaller..."

# Stop running instance if present
echo "Attempting to stop running Ron Bot instance (if any)..."
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
if [ -x "$SCRIPT_DIR/stop_ron.sh" ]; then
  "$SCRIPT_DIR/stop_ron.sh" -f || true
fi

# Remove global symlinks
for name in ron-start ron-stop ron-status; do
  LINK="/usr/local/bin/$name"
  if [ -L "$LINK" ] || [ -e "$LINK" ]; then
    if [ -w "$(dirname "$LINK")" ]; then
      rm -f "$LINK"
      echo "Removed $LINK"
    else
      if [ "$FORCE" -eq 1 ]; then
        sudo rm -f "$LINK" || true
        echo "Removed $LINK (sudo used)"
      else
        echo "$LINK exists but requires sudo to remove. Proceed? (y/N)"
        read -r ans
        case "$ans" in
          [Yy]|[Yy][Ee][Ss])
            sudo rm -f "$LINK"
            echo "Removed $LINK"
            ;;
          *) echo "Skipped $LINK" ;;
        esac
      fi
    fi
  else
    echo "$LINK not found; skipping."
  fi
done

# Remove man page
MAN_FILE="/usr/local/share/man/man1/ron.1"
if [ -f "$MAN_FILE" ]; then
  if [ -w "$(dirname "$MAN_FILE")" ]; then
    rm -f "$MAN_FILE"
    echo "Removed $MAN_FILE"
  else
    if [ "$FORCE" -eq 1 ]; then
      sudo rm -f "$MAN_FILE" || true
      echo "Removed $MAN_FILE (sudo used)"
    else
      echo "$MAN_FILE exists but requires sudo to remove. Proceed? (y/N)"
      read -r ans
      case "$ans" in
        [Yy]|[Yy][Ee][Ss])
          sudo rm -f "$MAN_FILE"
          echo "Removed $MAN_FILE"
          ;;
        *) echo "Skipped removing man page" ;;
      esac
    fi
  fi
else
  echo "$MAN_FILE not found; skipping."
fi

# Try to update man database
if command -v mandb >/dev/null 2>&1; then
  mandb 2>/dev/null || true
fi

# Disable and remove systemd user service if present
if command -v systemctl >/dev/null 2>&1; then
  UNIT_FILE="$HOME/.config/systemd/user/ron.service"
  if [ -f "$UNIT_FILE" ]; then
    if [ "$FORCE" -eq 1 ]; then
      systemctl --user disable --now ron.service 2>/dev/null || true
      rm -f "$UNIT_FILE"
      systemctl --user daemon-reload 2>/dev/null || true
      echo "Removed systemd service $UNIT_FILE"
    else
      echo "Found systemd user service at $UNIT_FILE. Remove it? (y/N)"
      read -r ans
      case "$ans" in
        [Yy]|[Yy][Ee][Ss])
          systemctl --user disable --now ron.service 2>/dev/null || true
          rm -f "$UNIT_FILE"
          systemctl --user daemon-reload 2>/dev/null || true
          echo "Removed systemd service"
          ;;
        *) echo "Skipped removing systemd service" ;;
      esac
    fi
  fi
fi

# Remove .venv if requested
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ "$REMOVE_VENV" -eq 1 ]; then
  if [ -d "$PROJECT_ROOT/.venv" ]; then
    if [ "$FORCE" -eq 1 ]; then
      rm -rf "$PROJECT_ROOT/.venv"
      echo "Removed .venv"
    else
      echo "Remove .venv? (y/N)"
      read -r ans
      case "$ans" in
        [Yy]|[Yy][Ee][Ss])
          rm -rf "$PROJECT_ROOT/.venv"
          echo "Removed .venv"
          ;;
        *) echo "Skipped removing .venv" ;;
      esac
    fi
  else
    echo ".venv not found; skipping."
  fi
fi

echo ""
echo "Uninstall complete."
echo "Note: .env and source files were not removed."
exit 0
