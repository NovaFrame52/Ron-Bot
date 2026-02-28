# Developer Notes — Ron v2.5.0

Purpose
- v2.5.0 builds on the wellness/moderation foundation with user statistics,
  leaderboard functionality, and improved startup reliability. The previous
  weather feature remains deprecated.

Important changes
- `scripts/ron_bot.py`
  - Added `stats`, `leaderboard`, and owner-only `health` commands.
  - Added startup guard and clearer dotenv import errors.
  - Help/about embeds updated to list new commands; various doc strings
    adjusted.
- `scripts/run_ron.sh` and `scripts/run.sh` modified to call the venv python
  explicitly.

Developer checklist after pulling v2.0.0
1. Update your virtualenv and install requirements:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Rebuild and run the bot locally:
```bash
python3 scripts/ron_bot.py
```
3. If you change commands, run `!sync` in a guild where the bot owner is present to sync slash commands.

Notes
- If you need weather functionality again, consider adding a separate optional plugin module and reintroducing `requests` behind a feature flag.
- Keep `DEVNOTES.md` for internal notes. User-facing docs are in `README.md`.
