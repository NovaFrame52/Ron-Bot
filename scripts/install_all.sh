#!/usr/bin/env bash
set -euo pipefail

# Full installer for Ron Bot
# Usage: ./install_all.sh [-f|--force] [--no-symlinks] [--no-desktop] [--skip-venv] [--install-man]
# -f, --force: non-interactive (assume yes)
# --no-symlinks: don't install global symlinks (/usr/local/bin)
# --no-desktop: don't copy .desktop launcher to Desktop
# --skip-venv: skip virtualenv creation and pip install
# --install-man: install man page to /usr/local/share/man/man1

FORCE=0
SYMLINKS=1
DESKTOP=1
SKIP_VENV=0
INSTALL_MAN=0

while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force) FORCE=1; shift ;;
    --no-symlinks) SYMLINKS=0; shift ;;
    --no-desktop) DESKTOP=0; shift ;;
    --skip-venv) SKIP_VENV=1; shift ;;
    --install-man) INSTALL_MAN=1; shift ;;
    -h|--help) echo "Usage: $0 [-f|--force] [--no-symlinks] [--no-desktop] [--skip-venv] [--install-man]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

echo "Starting Ron Bot installer..."

# Resolve script and project root so installer works from any CWD or when invoked via symlink
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# Work in project root
cd "$PROJECT_ROOT" || true

# Check python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 not found. Please install Python 3.8+" >&2
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Using Python $PYTHON_VERSION"

# Create virtualenv and install requirements (in project root)
if [ "$SKIP_VENV" -eq 0 ]; then
  if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "Creating virtualenv..."
    python3 -m venv "$PROJECT_ROOT/.venv"
  else
    echo "Virtualenv .venv already exists."
  fi

  # Activate
  # shellcheck disable=SC1091
  . "$PROJECT_ROOT/.venv/bin/activate"

  echo "Installing dependencies..."
  # Bootstrap pip if not available
  python3 -m ensurepip --upgrade 2>/dev/null || true
  python3 -m pip install --upgrade pip
  python3 -m pip install -r "$PROJECT_ROOT/requirements.txt"
else
  echo "Skipping virtualenv and dependency installation (per --skip-venv)."
fi

# Make helper scripts executable (scripts/ directory)
for f in "$SCRIPT_DIR"/run_ron.sh "$SCRIPT_DIR"/stop_ron.sh "$SCRIPT_DIR"/install_systemd_user.sh "$SCRIPT_DIR"/install_man.sh; do
  if [ -f "$f" ]; then
    chmod +x "$f"
  fi
done

# Ensure .env.example exists
if [ ! -f "$PROJECT_ROOT/.env.example" ]; then
  cat > "$PROJECT_ROOT/.env.example" <<'EOF'
# Example environment for Ron Bot
DISCORD_TOKEN=your_token_here
PREFIX=!
EOF
  echo "Created .env.example"
fi

# If .env missing, offer to create it from example
if [ ! -f "$PROJECT_ROOT/.env" ]; then
  if [ "$FORCE" -eq 1 ]; then
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo "Created .env from .env.example"
  else
    echo ".env not found. Create it from .env.example? (y/N)"
    read -r ans
    case "$ans" in
      [Yy]|[Yy][Ee][Ss])
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        echo "Created .env from .env.example"
        ;;
      *) echo "Skipped creating .env" ;;
    esac
  fi
fi

# Secure .env if present
if [ -f "$PROJECT_ROOT/.env" ]; then
  current_perm="$(stat -c %a "$PROJECT_ROOT/.env" 2>/dev/null || echo "")"
  if [ "$current_perm" != "600" ]; then
    chmod 600 "$PROJECT_ROOT/.env"
    echo "Secured .env with permissions 600"
  fi
else
  echo "Note: .env not found. Create it with your DISCORD_TOKEN if you haven't already."
fi

# Install symlinks
if [ "$SYMLINKS" -eq 1 ]; then
  echo "Installing global symlinks..."
  for name in ron-start ron-stop ron-status; do
    LINK="/usr/local/bin/$name"
    case "$name" in
      ron-start) SCRIPT="$SCRIPT_DIR/run_ron.sh" ;;
      ron-stop) SCRIPT="$SCRIPT_DIR/stop_ron.sh" ;;
      ron-status) SCRIPT="$SCRIPT_DIR/ron-status.sh" ;;
    esac
    if [ ! -f "$SCRIPT" ]; then
      continue
    fi
    if [ ! -x "$SCRIPT" ]; then
      chmod +x "$SCRIPT"
    fi
    if [ -w "$(dirname "$LINK")" ]; then
      ln -sf "$SCRIPT" "$LINK"
      echo "  Installed $LINK"
    else
      if [ "$FORCE" -eq 1 ]; then
        sudo ln -sf "$SCRIPT" "$LINK"
        echo "  Installed $LINK (sudo)"
      else
        echo "  $LINK requires sudo. Create it? (y/N)"
        read -r ans
        case "$ans" in
          [Yy]|[Yy][Ee][Ss])
            sudo ln -sf "$SCRIPT" "$LINK"
            echo "  Installed $LINK"
            ;;
          *) echo "  Skipped $LINK" ;;
        esac
      fi
    fi
  done
fi

# Install man page
if [ "$INSTALL_MAN" -eq 1 ]; then
  echo "Installing man page..."
  if [ -x "$SCRIPT_DIR/install_man.sh" ]; then
    if [ "$FORCE" -eq 1 ]; then
      "$SCRIPT_DIR/install_man.sh" -f
    else
      "$SCRIPT_DIR/install_man.sh"
    fi
  fi
fi

# Summary
echo ""
echo "Installation complete. Quick setup:"
if [ -f "$PROJECT_ROOT/.env" ]; then
  echo "✓ .env exists"
  if grep -q "your_token_here" "$PROJECT_ROOT/.env" 2>/dev/null; then
    echo "  ⚠ .env still has placeholder DISCORD_TOKEN — update it with your real token"
  else
    echo "  ✓ DISCORD_TOKEN appears to be set"
  fi
else
  echo "✗ .env needs to be created with your DISCORD_TOKEN"
fi
echo ""
echo "To start Ron Bot:"
if [ "$SYMLINKS" -eq 1 ]; then
  echo "  ron-start     (or ./scripts/run_ron.sh)"
else
  echo "  ./scripts/run_ron.sh"
fi
echo ""
echo "To stop Ron Bot:"
if [ "$SYMLINKS" -eq 1 ]; then
  echo "  ron-stop      (or ./scripts/stop_ron.sh)"
else
  echo "  ./scripts/stop_ron.sh"
fi
echo ""
echo "To install systemd --user service:"
echo "  ./scripts/install_systemd_user.sh"
echo ""
echo "To install man page:"
echo "  ./scripts/install_man.sh"
echo "  (or re-run this installer with --install-man flag)"
echo ""
echo "For help in Discord:"
echo "  !help or /help"
echo ""
echo "Done."
exit 0
