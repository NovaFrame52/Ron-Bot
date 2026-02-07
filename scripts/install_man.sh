#!/usr/bin/env bash
set -euo pipefail

# Install man page for Ron Bot to system location
# Usage: ./install_man.sh [-f|--force]

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
MAN_SOURCE="$PROJECT_ROOT/ron.1"
MAN_DIR="/usr/local/share/man/man1"
MAN_FILE="$MAN_DIR/ron.1"

if [ ! -f "$MAN_SOURCE" ]; then
  echo "Error: ron.1 man page not found at $MAN_SOURCE" >&2
  exit 1
fi

# Create man directory if needed
if [ ! -d "$MAN_DIR" ]; then
  echo "Creating man directory: $MAN_DIR"
  sudo mkdir -p "$MAN_DIR" || {
    echo "Error: Could not create $MAN_DIR" >&2
    exit 1
  }
fi

# Check if we need sudo
if [ -w "$MAN_DIR" ]; then
  cp "$MAN_SOURCE" "$MAN_FILE"
  echo "Installed man page to $MAN_FILE"
else
  if [ "$FORCE" -eq 1 ]; then
    sudo cp "$MAN_SOURCE" "$MAN_FILE"
    echo "Installed man page to $MAN_FILE (sudo used)"
  else
    echo "Installing to $MAN_DIR requires sudo."
    read -r -p "Proceed? (y/N) " answer
    case "$answer" in
      [Yy]|[Yy][Ee][Ss])
        sudo cp "$MAN_SOURCE" "$MAN_FILE"
        echo "Installed man page to $MAN_FILE"
        ;;
      *) echo "Skipped man page installation"; exit 0 ;;
    esac
  fi
fi

# Try to update man database
if command -v mandb >/dev/null 2>&1; then
  echo "Updating man database..."
  mandb 2>/dev/null || true
fi

echo "Man page installation complete."
echo "You can now view it with: man ron"
exit 0
