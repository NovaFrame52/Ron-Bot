#!/usr/bin/env bash
set -e
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
python3 ron_bot.py
