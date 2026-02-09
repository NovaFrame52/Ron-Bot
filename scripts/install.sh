#!/usr/bin/env bash
set -euo pipefail

# Merged installer for Ron Bot
# Combines install_all.sh, install_man.sh, and install_systemd_user.sh
# Usage: ./install.sh [-f|--force] [--no-symlinks] [--no-desktop] [--skip-venv] [--skip-systemd] [--enable-linger]
# -f, --force: non-interactive (assume yes)
# --no-symlinks: don't install global symlinks (/usr/local/bin)
# --skip-venv: skip virtualenv creation and pip install
# --skip-systemd: skip systemd --user service installation
# --enable-linger: enable systemd linger for user

FORCE=0
SYMLINKS=1
SKIP_VENV=0
SKIP_SYSTEMD=0
ENABLE_LINGER=0

while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force) FORCE=1; shift ;;
    --no-symlinks) SYMLINKS=0; shift ;;
    --skip-venv) SKIP_VENV=1; shift ;;
    --skip-systemd) SKIP_SYSTEMD=1; shift ;;
    --enable-linger) ENABLE_LINGER=1; shift ;;
    -h|--help) echo "Usage: $0 [-f|--force] [--no-symlinks] [--skip-venv] [--skip-systemd] [--enable-linger]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

echo "Starting Ron Bot installer..."

# Resolve script and project root
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT" || true

# Check python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 not found. Please install Python 3.8+" >&2
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Using Python $PYTHON_VERSION"

# ==== VIRTUALENV & DEPENDENCIES ====
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
  python3 -m ensurepip --upgrade 2>/dev/null || true
  python3 -m pip install --upgrade pip
  python3 -m pip install -r "$PROJECT_ROOT/requirements.txt"
else
  echo "Skipping virtualenv and dependency installation (per --skip-venv)."
fi

# Make helper scripts executable
for f in "$SCRIPT_DIR"/run_ron.sh "$SCRIPT_DIR"/stop_ron.sh "$SCRIPT_DIR"/install_systemd_user.sh; do
  if [ -f "$f" ]; then
    chmod +x "$f"
  fi
done

# ==== ENVIRONMENT SETUP ====
if [ ! -f "$PROJECT_ROOT/.env.example" ]; then
  cat > "$PROJECT_ROOT/.env.example" <<'EOF'
# Example environment for Ron Bot
DISCORD_TOKEN=your_token_here
PREFIX=!
EOF
  echo "Created .env.example"
fi

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

# ==== GLOBAL SYMLINKS ====
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

# ==== MAN PAGE ====
echo "Installing man page..."
MAN_SOURCE="$PROJECT_ROOT/ron.1"
MAN_DIR="/usr/local/share/man/man1"
MAN_FILE="$MAN_DIR/ron.1"

if [ -f "$MAN_SOURCE" ]; then
  if [ ! -d "$MAN_DIR" ]; then
    echo "Creating man directory: $MAN_DIR"
    sudo mkdir -p "$MAN_DIR" || {
      echo "Error: Could not create $MAN_DIR" >&2
      exit 1
    }
  fi

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
        *) echo "Skipped man page installation" ;;
      esac
    fi
  fi

  if command -v mandb >/dev/null 2>&1; then
    echo "Updating man database..."
    mandb 2>/dev/null || true
  fi
else
  echo "Warning: ron.1 man page not found at $MAN_SOURCE"
fi

# ==== SYSTEMD --USER SERVICE ====
if [ "$SKIP_SYSTEMD" -eq 0 ]; then
  echo "Installing systemd --user service..."
  if command -v systemctl >/dev/null 2>&1; then
    UNIT_DIR="$HOME/.config/systemd/user"
    UNIT_FILE="$UNIT_DIR/ron.service"

    mkdir -p "$UNIT_DIR"

    cat > "$UNIT_FILE" <<EOF
[Unit]
Description=Ron Bot (weather and wellness)
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_ROOT
ExecStart=$SCRIPT_DIR/run_ron.sh -f
# Load environment from .env if present
EnvironmentFile=$PROJECT_ROOT/.env
Restart=on-failure
RestartSec=5
# Capture output to journal
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ron-bot

[Install]
WantedBy=default.target
EOF

    echo "Installed systemd user unit to $UNIT_FILE"

    # Reload and enable
    systemctl --user daemon-reload
    systemctl --user enable --now ron.service

    if [ $? -eq 0 ]; then
      echo "ron.service enabled and started (systemd --user)."
    else
      echo "Failed to enable/start ron.service; check 'systemctl --user status ron.service' for details." >&2
    fi

    if [ "$ENABLE_LINGER" -eq 1 ]; then
      if command -v loginctl >/dev/null 2>&1; then
        if [ "$FORCE" -eq 1 ]; then
          sudo loginctl enable-linger "$USER" 2>/dev/null || true
          echo "Enabled linger for $USER (sudo used)."
        else
          echo "Enable linger for $USER to allow services to run without active login? (y/N)"
          read -r ans
          case "$ans" in
            [Yy]|[Yy][Ee][Ss])
              sudo loginctl enable-linger "$USER"
              echo "Enabled linger for $USER"
              ;;
            *) echo "Skipped enabling linger" ;;
          esac
        fi
      else
        echo "loginctl not found; cannot enable linger" >&2
      fi
    fi
  else
    echo "systemctl not found; skipping systemd --user service installation" >&2
  fi
fi

# ==== SUMMARY ====
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
if [ "$SKIP_SYSTEMD" -eq 0 ] && command -v systemctl >/dev/null 2>&1; then
  echo "To manage systemd service:"
  echo "  systemctl --user status ron.service"
  echo "  systemctl --user start/stop/restart ron.service"
  echo ""
fi
echo "For help in Discord:"
echo "  !help or /help"
echo ""
echo "Done."
exit 0
