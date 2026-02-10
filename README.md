# Ron — Discord Bot (v2.0.0)

Ron v2.0.0 focuses the project on wellness features and moderation utilities. The weather feature was removed to streamline the bot for communities who want hydration, motivation, and moderation tools.

Highlights
- 💧 Improved hydration reminders with many friendly phrases
- 💪 Expanded affirmations, workouts, breathing exercises, and wellness tips
- 🧹 `purge` — moderator bulk-delete messages
- 📢 `announce` — moderator channel announcements

Quick Start
1. Install (recommended):

```bash
cd scripts
./install.sh
```

2. Configure `.env` (set `DISCORD_TOKEN` and optional `PREFIX`).

3. Run the bot:

```bash
python3 scripts/ron_bot.py
```

Core Commands
- `!waterreminder` / `/waterreminder`: subscribe/unsubscribe to hourly hydration DMs
- `!motivate` / `/motivate`: receive a motivational affirmation
- `!workout` / `/workout`: get a short workout suggestion
- `!breathing` / `/breathing`: guided breathing exercise
- `!tip` / `/tip`: daily wellness tip
- `!roll NdM` / `/roll NdM`: roll dice (e.g., `2d6`, `d20`)
- `!remind <minutes> <message>` / `/remind`: personal DM reminder

Moderator Commands (server mods only)
- `!purge <count>` / `/purge <count>`: bulk-delete up to 100 messages
- `!announce <#channel> <message>` / `/announce`: post a highlighted announcement embed to a channel

Files
- `scripts/ron_bot.py` — main bot implementation
- `CHANGELOG.md`, `releasenotes.md`, `GITHUB_RELEASE.md` — release artifacts for v2.0.0
- `DEVNOTES.md` — developer notes and migration guidance

Notes
- Weather functionality removed in v2.0.0. Use wellness features instead.
- Both prefix (`!`) and slash (`/`) commands are supported.

Requirements
- Python 3.8+
- `discord.py` >= 2.0.0
- `python-dotenv`

Developer
- See `DEVNOTES.md` for developer setup and migration notes.
