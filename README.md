# Ron — Discord Bot

Ron is a friendly Discord bot that provides weather information, wellness reminders, motivational features, and quality-of-life enhancements.

## Features

- 🌍 **Weather** - Get real-time weather for any city
- 💧 **Hydration Reminders** - Auto-reminders to drink water hourly
- 💪 **Wellness** - Workouts, breathing exercises, and wellness tips
- 🎯 **Motivation** - Affirmations and motivational quotes
- 🎲 **Fun** - Dice rolling and games
- ⏰ **Reminders** - Personal reminder system
- ✨ **QOL Features** - Help, About, Sync, and more

## Commands

### Weather & Location
- `/weather <city>` or `!weather <city>` - Get current weather with temperature, humidity, wind speed, and emojis

### Fun & Games
- `/ping` or `!ping` - Check bot latency
- `/roll NdM` or `!roll NdM` - Roll dice (e.g., `2d6`, `d20`). Supports up to 100 dice.
- `/quote` or `!quote` - Random motivational quote from 22+ inspirational sources

### Wellness & Health
- `/waterreminder` or `!waterreminder` - Subscribe/unsubscribe from hourly water reminders
- `/workout` or `!workout` - Quick random workout suggestion (2-min stretches to full yoga flows)
- `/breathing` or `!breathing` - Guided breathing exercises (Box Breathing, 4-7-8, Belly Breathing, Energizing)
- `/tip` or `!tip` - Daily wellness tips covering sleep, nutrition, movement, mindfulness, and more
- `/motivate` or `!motivate` - Quick motivational affirmation boost

### Reminders
- `/remind <minutes> <message>` or `!remind <minutes> <message>` - Set a personal DM reminder
  - Example: `/remind 10 Take a break` or `!remind 30 Stretch and hydrate`

### Information & Management
- `/help` or `!help` - Show all available commands with descriptions
- `/about` or `!about` - About Ron Bot and its features
- `!sync` - Manually sync slash commands with Discord (owner-only)

## Installation

### Quick Setup (Recommended)

```bash
cd scripts
./install_all.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Set up environment configuration
- Create convenient symlinks (`ron-start`, `ron-stop`, `ron-status`)

### Manual Setup

1. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set configuration:
```bash
cp .env.example .env
# Edit .env and add your DISCORD_TOKEN
```

4. Run the bot:
```bash
python3 ron_bot.py
```

## Usage

### Starting & Stopping

Using symlinks (if installed):
```bash
ron-start      # Start Ron Bot
ron-stop       # Stop Ron Bot
ron-status     # Check status
```

Or directly:
```bash
./scripts/run_ron.sh     # Start
./scripts/stop_ron.sh    # Stop
./scripts/ron-status.sh  # Status
```

### Systemd Integration (Optional)

Auto-start Ron on login:
```bash
./scripts/install_systemd_user.sh
systemctl --user enable ron.service
```

Then manage with:
```bash
systemctl --user start ron.service
systemctl --user stop ron.service
systemctl --user status ron.service
```

### Syncing Commands

After updating commands, sync with Discord:
```bash
!sync
```

Or in Discord: `!sync`

## Uninstallation

```bash
./scripts/uninstall_all.sh
```

Add `--remove-venv` to also delete the virtual environment.

## Configuration

### Environment Variables

- `DISCORD_TOKEN` — Your Discord bot token (required)
- `PREFIX` — Command prefix, default is `!` (optional)

Example `.env`:
```
DISCORD_TOKEN=your_actual_token_here
PREFIX=!
```

## Features in Detail

### Water Reminder System
Subscribe to hourly hydration reminders sent via DM. The bot sends random encouragement messages to keep you healthy and hydrated throughout the day.

### Wellness Content
- **12 Affirmations** - Motivational messages for daily boosts
- **10 Workout Ideas** - From quick desk stretches to full yoga flows
- **4 Breathing Exercises** - Stress relief and calming techniques
- **12 Wellness Tips** - Covering sleep, nutrition, movement, mindfulness, and more

### Weather API
Uses the free **wttr.in API** - no API key required! Provides accurate weather data for any city worldwide with emoji indicators and detailed metrics.

## Requirements

- Python 3.8+
- discord.py >= 2.0.0
- python-dotenv
- requests

## Setup Notes

- Ensure your bot has **Message Content Intent** enabled in Discord Developer Portal
- For water reminders to work, users must have DMs enabled
- Weather data updates in real-time from the free API
- All commands support both prefix (`!`) and slash (`/`) formats

## Troubleshooting

### Bot won't start
- Check `.env` has valid `DISCORD_TOKEN`
- Verify Python 3.8+ is installed
- Check logs: `tail -f ron.log`

### Commands not appearing
- Run `!sync` to sync slash commands
- Ensure bot has `applications.commands` scope in Discord

### Water reminders not working
- Ensure user has DMs enabled
- Check bot has permission to DM users
- Verify user subscribed with `!waterreminder`

## Logs

Bot logs are saved to `ron.log` in the project root. View with:
```bash
tail -f ron.log
```

## Support

For issues, check the logs and verify:
1. DISCORD_TOKEN is valid
2. Bot has required intents enabled
3. Network connection is stable

For Suggestions, open an issue or submit a pull request.

---

**Made with ❤️ for wellness and productivity**

Stay hydrated, stay healthy! 💚



