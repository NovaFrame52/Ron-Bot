# Ron — Discord Bot (v2.5.0)

(This release adds statistics commands and health reporting; see the changelog for details.)

Ron v2.5.0 builds on the wellness and moderation focus with new
user‑stats and health reporting features. The weather functionality was
removed in earlier releases to keep the bot lightweight and targeted.

Highlights
- � New user stats (`stats`), leaderboard, and owner health check commands
- �💧 Improved hydration reminders with many friendly phrases
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

Additional user commands:
- `!stats` / `/stats`: view your reminder stats
- `!leaderboard` / `/leaderboard`: see top streaks

Owner-only commands:
- `!health` / `/health`: bot status and resource usage

Moderator Commands (server mods only)
- `!purge <count>` / `/purge <count>`: bulk-delete up to 100 messages
- `!announce <#channel> <message>` / `/announce`: post a highlighted announcement embed to a channel

Files
- `scripts/ron_bot.py` — main bot implementation
- `CHANGELOG.md` — history of changes
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
