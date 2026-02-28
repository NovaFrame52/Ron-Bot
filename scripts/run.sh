#!/usr/bin/env bash
set -e
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
# prefer the venv python if available
if [ -x ".venv/bin/python" ]; then
  .venv/bin/python ron_bot.py
else
  python3 ron_bot.py
fi
