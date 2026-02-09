#!/usr/bin/env bash
set -euo pipefail

# Update Ron Bot from GitHub repository
# Usage: ./update.sh [-f|--force] [--no-restart]
# -f, --force: non-interactive (assume yes)
# --no-restart: don't restart the service after update

FORCE=0
RESTART=1
REPO_URL="https://github.com/NovaFrame52/Ron-Bot.git"

while [ $# -gt 0 ]; do
  case "$1" in
    -f|--force) FORCE=1; shift ;;
    --no-restart) RESTART=0; shift ;;
    -h|--help) echo "Usage: $0 [-f|--force] [--no-restart]"; exit 0 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

echo "Starting Ron Bot update..."

# Resolve script and project root
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT" || true

# Check if .git exists
if [ ! -d "$PROJECT_ROOT/.git" ]; then
  echo "Error: Not a git repository. Initialize with: git clone $REPO_URL" >&2
  exit 1
fi

# Verify we're on the right repo
CURRENT_REPO=$(git -C "$PROJECT_ROOT" config --get remote.origin.url 2>/dev/null || echo "")
if [ "$CURRENT_REPO" != "$REPO_URL" ]; then
  echo "Warning: Current remote URL ($CURRENT_REPO) differs from expected ($REPO_URL)"
  if [ "$FORCE" -ne 1 ]; then
    read -r -p "Continue anyway? (y/N) " answer
    case "$answer" in
      [Yy]|[Yy][Ee][Ss]) ;;
      *) exit 1 ;;
    esac
  fi
fi

# Check for uncommitted changes
if ! git -C "$PROJECT_ROOT" diff-index --quiet HEAD -- 2>/dev/null; then
  echo "Warning: Repository has uncommitted changes"
  if [ "$FORCE" -ne 1 ]; then
    read -r -p "Stash changes and continue? (y/N) " answer
    case "$answer" in
      [Yy]|[Yy][Ee][Ss])
        git -C "$PROJECT_ROOT" stash
        echo "Changes stashed"
        ;;
      *) exit 1 ;;
    esac
  else
    git -C "$PROJECT_ROOT" stash
    echo "Changes stashed (--force)"
  fi
fi

# Fetch latest from remote
echo "Fetching latest from $REPO_URL..."
git -C "$PROJECT_ROOT" fetch origin

# Get current and upstream branches
CURRENT_BRANCH=$(git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD)
UPSTREAM_BRANCH="origin/$CURRENT_BRANCH"

# Check if upstream exists
if ! git -C "$PROJECT_ROOT" rev-parse "$UPSTREAM_BRANCH" >/dev/null 2>&1; then
  echo "Warning: Upstream branch $UPSTREAM_BRANCH does not exist"
  UPSTREAM_BRANCH="origin/main"
  echo "Trying $UPSTREAM_BRANCH instead..."
  if ! git -C "$PROJECT_ROOT" rev-parse "$UPSTREAM_BRANCH" >/dev/null 2>&1; then
    UPSTREAM_BRANCH="origin/master"
    echo "Trying $UPSTREAM_BRANCH instead..."
  fi
fi

# Check if updates are available
LOCAL=$(git -C "$PROJECT_ROOT" rev-parse HEAD)
REMOTE=$(git -C "$PROJECT_ROOT" rev-parse "$UPSTREAM_BRANCH")

if [ "$LOCAL" = "$REMOTE" ]; then
  echo "✓ Already up to date"
else
  echo "Updates available. Pulling from $UPSTREAM_BRANCH..."
  git -C "$PROJECT_ROOT" pull origin "$CURRENT_BRANCH"
  echo "✓ Repository updated"
fi

# ==== UPDATE DEPENDENCIES ====
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
  echo "Updating Python dependencies..."
  
  if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    . "$PROJECT_ROOT/.venv/bin/activate"
    python3 -m pip install --upgrade pip
    python3 -m pip install -r "$PROJECT_ROOT/requirements.txt"
    echo "✓ Dependencies updated"
  else
    echo "Warning: Virtual environment not found at .venv"
    echo "Run: ./scripts/install.sh --skip-man --skip-systemd"
    exit 1
  fi
else
  echo "Warning: requirements.txt not found"
fi

# ==== RESTART SERVICE ====
if [ "$RESTART" -eq 1 ]; then
  if command -v systemctl >/dev/null 2>&1; then
    if systemctl --user is-enabled ron.service >/dev/null 2>&1; then
      echo "Restarting ron.service..."
      systemctl --user restart ron.service
      if [ $? -eq 0 ]; then
        echo "✓ Service restarted"
      else
        echo "Warning: Failed to restart service. Check manually with: systemctl --user status ron.service" >&2
      fi
    else
      echo "Note: ron.service not enabled in systemd --user. If running manually, restart scripts/run_ron.sh"
    fi
  else
    echo "Note: systemctl not found. Restart Ron Bot manually if needed"
  fi
else
  echo "Note: Restart skipped (--no-restart). Restart Ron Bot manually when ready"
fi

echo ""
echo "✓ Update complete"
echo ""
exit 0
