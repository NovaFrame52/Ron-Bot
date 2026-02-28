import os
import json
import random
import asyncio
from pathlib import Path

# dotenv is optional for users running from the venv; if the import fails we
# want a clear message instead of a confusing traceback later when TOKEN is
# missing.  We'll try to import it and give an actionable error if it's
# unavailable.  The run scripts (and instructions in README) should make sure
# the virtual environment is activated or the correct interpreter is used.
try:
    from dotenv import load_dotenv
except ImportError as exc:
    raise ImportError(
        "python-dotenv is not installed. "
        "Run `pip install -r requirements.txt` (inside the project's venv) "
        "or use the provided scripts (`./scripts/run_ron.sh`)."
    ) from exc

import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
import logging
import psutil

# Define ROOT first
ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "configs.json"
REMINDER_STORAGE_PATH = ROOT / "reminders.json"

# Load .env BEFORE any validation
load_dotenv(dotenv_path=ROOT / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")

# Now validate .env variables
required_env_vars = ["DISCORD_TOKEN"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

if not TOKEN:
    raise EnvironmentError("DISCORD_TOKEN is not set in the .env file.")

# Initialize reminders from persistent storage
def load_reminders():
    if REMINDER_STORAGE_PATH.exists():
        try:
            return json.loads(REMINDER_STORAGE_PATH.read_text())
        except Exception:
            return {}
    return {}

def save_reminders(reminders: dict):
    REMINDER_STORAGE_PATH.write_text(json.dumps(reminders, indent=2))

reminders = load_reminders()

ALLOWED_DM_USER_ID = 821102915325526046

# Define DEFAULT_PREFIX (already defined above, but ensure it exists)
if 'DEFAULT_PREFIX' not in locals():
    DEFAULT_PREFIX = os.getenv("PREFIX", "!")

# Initialize WATER_REMINDER_USERS as a set
WATER_REMINDER_USERS = set()

# Define WATER_REMINDER_PHRASES
WATER_REMINDER_PHRASES = [
    "💧 Time to drink some water! Stay hydrated.",
    "🚰 Hydration check: have a glass of water now!",
    "💦 Quick reminder: water helps your focus and mood.",
    "🧊 Take a sip of water and stretch your shoulders.",
    "🥤 Hydrate! Small sips often beat one large drink.",
    "💧 Feeling thirsty? Drink up and breathe deeply.",
    "🍋 Try water with a slice of lemon for a refreshing boost.",
    "💧 Keep a water bottle nearby — sip frequently!",
    "🔔 Hydration reminder: 1 glass now, another in an hour!",
    "💚 Water helps your body and mind — take a drink.",
    "💧 Quick goal: drink 250ml of water in the next 10 minutes.",
    "⚡ Boost your energy: stand up and drink some water.",
]

# Define QUOTES
QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It is during our darkest moments that we must focus to see the light. - Aristotle",
    "The only impossible journey is the one you never begin. - Tony Robbins",
    "Success is not final, failure is not fatal. - Winston Churchill",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Do what you can, with what you have, where you are. - Theodore Roosevelt",
    "Excellence is not a skill, it's an attitude. - Ralph Marston",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "Your limitation—it's only your imagination. Push beyond limitations.",
    "Great things never come from comfort zones. - Unknown",
    "Dream it. Wish it. Do it. - Unknown",
    "Success doesn't just find you. You have to go out and get it. - Unknown",
    "The harder you work for something, the greater you'll feel when you achieve it. - Unknown",
    "Dream bigger. Do bigger. - Unknown",
    "Don't stop when you're tired. Stop when you're done. - Unknown",
    "Wake up with determination. Go to bed with satisfaction. - Unknown",
    "Do something today that your future self will thank you for. - Sean Patrick Flanery",
    "Little things? There are no little things. - Unknown",
    "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
]

# Define AFFIRMATIONS
AFFIRMATIONS = [
    "You are capable of amazing things. 💪",
    "Your potential is limitless — keep taking steps. ✨",
    "You are stronger and kinder than you give yourself credit for. 🌟",
    "Small progress is still progress. Celebrate it. 🎉",
    "You deserve rest, joy, and success. 🎯",
    "Your presence matters to others, even when you doubt it. 💖",
    "Challenges grow you; you're doing the work. 🌱",
    "Breathe, reset, continue — you have this. 🧘",
    "You are resilient, resourceful, and learning daily. 🏆",
    "Today is a fresh start — be curious and kind. ☀️",
    "Your actions create ripples — keep going. 🤝",
    "Dream, plan, act — one step at a time. 💭",
    "Small acts of self-care compound into big change. 🌿",
    "You belong and you are enough, exactly as you are. 💚",
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def determine_prefix(bot, message):
    prefix = os.getenv("PREFIX", "!")
    return commands.when_mentioned_or(prefix)(bot, message)



# Weather functionality removed in v2.0.0 — no fetch_weather implementation


bot = commands.Bot(command_prefix=determine_prefix, intents=intents, description="Ron - The friendly wellness and moderation assistant")
bot.water_reminder_task = None  # Will be set in on_ready()

# Disable the built-in help command so we can use our custom one
bot.remove_command("help")


@bot.event
async def on_ready():
    if bot.user:
        print(f"Ron is ready. Logged in as: {bot.user} (ID: {bot.user.id})")
    else:
        print("Ron is ready, but bot.user is not yet available.")
    try:
        await bot.tree.sync()
        print("Synced slash commands (bot.tree)")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
    # Start the water reminder background task
    if bot.water_reminder_task is not None and not bot.water_reminder_task.done():
        bot.water_reminder_task.cancel()
    bot.water_reminder_task = asyncio.create_task(water_reminder_loop(bot))



async def water_reminder_loop(bot):
    """Background task to send water reminders every hour."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            await asyncio.sleep(3600)  # Every hour
            for user_id in WATER_REMINDER_USERS.copy():
                try:
                    user = await bot.fetch_user(user_id)
                    await user.send(random.choice(WATER_REMINDER_PHRASES))
                except Exception:
                    WATER_REMINDER_USERS.discard(user_id)
        except asyncio.CancelledError:
            break
        except Exception:
            pass


def is_mod(ctx):
    return ctx.author.guild_permissions.administrator or ctx.author.guild.permissions.manage_guild


def is_mod_interaction(interaction: discord.Interaction):
    if not interaction.guild:
        return False
    user = interaction.user
    return user.guild.permissions.administrator or user.guild.permissions.manage_guild


@bot.command()
async def ping(ctx):
    """Responds with pong and latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! {latency}ms")


@bot.tree.command(name="ping")
async def slash_ping(interaction: discord.Interaction):
    """Slash version of ping."""
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! {latency}ms")


@bot.command()
async def roll(ctx, dice: str = "1d6"):
    """Roll dice using NdM format, e.g. 2d6 or d20."""
    try:
        if "d" not in dice:
            raise ValueError
        parts = dice.split("d")
        n = int(parts[0]) if parts[0] != "" else 1
        m = int(parts[1])
        if n < 1 or m < 1 or n > 100:
            raise ValueError
    except Exception:
        await ctx.send("Usage: !roll NdM (e.g. 2d6, d20). Max 100 dice.")
        return
    rolls = [random.randint(1, m) for _ in range(n)]
    total = sum(rolls)
    await ctx.send(f"🎲 Rolled {dice}: {rolls} (total: {total})")


@bot.tree.command(name="roll")
@app_commands.describe(dice="Dice to roll in NdM format, e.g. 2d6")
async def slash_roll(interaction: discord.Interaction, dice: str = "1d6"):
    try:
        if "d" not in dice:
            raise ValueError
        parts = dice.split("d")
        n = int(parts[0]) if parts[0] != "" else 1
        m = int(parts[1])
        if n < 1 or m < 1 or n > 100:
            raise ValueError
    except Exception:
        await interaction.response.send_message("Usage: /roll NdM (e.g. /roll 2d6). Max 100 dice.", ephemeral=True)
        return
    rolls = [random.randint(1, m) for _ in range(n)]
    total = sum(rolls)
    await interaction.response.send_message(f"🎲 Rolled {dice}: {rolls} (total: {total})")


@bot.command()
async def quote(ctx):
    """Send a random motivational quote."""
    await ctx.send(random.choice(QUOTES))


@bot.tree.command(name="quote")
async def slash_quote(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(QUOTES))


@bot.command()
async def remind(ctx, minutes: float, *, message: str):
    """Set a reminder for yourself: !remind 10 Take a break"""
    if minutes <= 0:
        await ctx.send("Please provide a positive number of minutes.")
        return
    await ctx.send(f"Okay {ctx.author.mention}, I'll remind you in {minutes} minute(s).")

    async def _reminder(delay, user, content):
        await asyncio.sleep(delay)
        try:
            await user.send(f"⏰ Reminder: {content}")
        except Exception:
            channel = None
            try:
                channel = discord.utils.get(user.guilds[0].text_channels, name="general")
            except Exception:
                pass
            if channel:
                await channel.send(f"{user.mention} ⏰ Reminder: {content}")

    asyncio.create_task(_reminder(minutes * 60, ctx.author, message))


@bot.tree.command(name="remind")
@app_commands.describe(minutes="Minutes until reminder", message="Reminder message")
async def slash_remind(interaction: discord.Interaction, minutes: float, message: str):
    if minutes <= 0:
        await interaction.response.send_message("Please provide a positive number of minutes.", ephemeral=True)
        return
    await interaction.response.send_message(f"Okay {interaction.user.mention}, I'll remind you in {minutes} minute(s).", ephemeral=True)

    async def _reminder(delay, user, content):
        await asyncio.sleep(delay)
        try:
            await user.send(f"⏰ Reminder: {content}")
        except Exception:
            try:
                channel = discord.utils.get(user.guilds[0].text_channels, name="general")
            except Exception:
                channel = None
            if channel:
                await channel.send(f"{user.mention} ⏰ Reminder: {content}")

    asyncio.create_task(_reminder(minutes * 60, interaction.user, message))


@bot.command(name="dm")
async def dm(ctx, member: discord.Member, *, message: str):
    """Send a DM to another member (restricted to invoker user ID 821102915325526046)."""
    # Restrict to invoker user ID
    if getattr(ctx.author, 'id', None) != ALLOWED_DM_USER_ID:
        await ctx.send("You are not allowed to use this command.")
        return
    # delete the invoking command message so only the invoker sees the result
    try:
        await ctx.message.delete()
    except Exception:
        pass

    # Check for an attachment on the invoking message
    attachment = None
    try:
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
    except Exception:
        attachment = None

    try:
        if attachment:
            file = await attachment.to_file()
            await member.send(content=message or None, file=file)
        else:
            # look for image URL in message
            import re
            m = re.search(r"(https?://\S+\.(?:png|jpg|jpeg|gif|webp))", message or "", re.IGNORECASE)
            if m:
                url = m.group(1)
                embed = discord.Embed()
                embed.set_image(url=url)
                await member.send(content=(message or None), embed=embed)
            else:
                await member.send(message or None)
        try:
            await ctx.author.send(f"Sent DM to {member.display_name}.")
        except Exception:
            pass
    except Exception as e:
        try:
            await ctx.author.send(f"Failed to send DM to {member.display_name}: {e}")
        except Exception:
            # last resort public error
            await ctx.send(f"Failed to send DM: {e}")


@bot.tree.command(name="dm")
@app_commands.describe(target="Member identifier (ID, mention, username#discrim, or name)", message="Message content")
async def slash_dm(interaction: discord.Interaction, target: str, message: str, image: discord.Attachment = None):
    # Ensure allowed user
    if getattr(interaction.user, 'id', None) != ALLOWED_DM_USER_ID:
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        return
    if not message:
        await interaction.response.send_message("Missing message content.", ephemeral=True)
        return
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
        return
    resolved = None
    tid = None
    # mention format
    if target.startswith("<@") and target.endswith(">"):
        digits = ''.join(c for c in target if c.isdigit())
        if digits:
            tid = digits
    elif target.isdigit():
        tid = target
    if tid:
        try:
            resolved = guild.get_member(int(tid))
        except Exception:
            resolved = None
    # username#discrim
    if resolved is None and "#" in target:
        name, discrim = target.rsplit("#", 1)
        for m in guild.members:
            if m.name == name and m.discriminator == discrim:
                resolved = m
                break
    # fallback: match display name or username
    if resolved is None:
        for m in guild.members:
            if m.display_name == target or m.name == target:
                resolved = m
                break
    if resolved is None:
        await interaction.response.send_message(f"Could not resolve target member: {target}. Use a mention, ID, or username#discrim.", ephemeral=True)
        return
    try:
        if image:
            file = await image.to_file()
            await resolved.send(content=message or None, file=file)
        else:
            import re
            m = re.search(r"(https?://\S+\.(?:png|jpg|jpeg|gif|webp))", message or "", re.IGNORECASE)
            if m:
                url = m.group(1)
                embed = discord.Embed()
                embed.set_image(url=url)
                await resolved.send(content=(message or None), embed=embed)
            else:
                await resolved.send(message or None)
        await interaction.response.send_message(f"Sent DM to {resolved.display_name}.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to send DM: {e}", ephemeral=True)


# The weather commands (prefix and slash) were removed in v2.0.0.


async def handle_waterreminder(user_id, interaction=None, ctx=None):
    """Shared handler for water reminder commands."""
    user_id = str(user_id)
    if user_id in reminders:
        del reminders[user_id]
        save_reminders(reminders)
        message = "💧 You've unsubscribed from water reminders."
        logging.info(f"User {user_id} unsubscribed from water reminders.")
    else:
        reminders[user_id] = {"subscribed": True}
        save_reminders(reminders)
        message = "💧 You've subscribed to hourly water reminders! Stay hydrated! 💪"
        logging.info(f"User {user_id} subscribed to water reminders.")

    if interaction:
        await interaction.response.send_message(message)
    elif ctx:
        await ctx.send(message)


@bot.command()
async def waterreminder(ctx):
    """Subscribe to hourly water reminders. Usage: !waterreminder"""
    await handle_waterreminder(ctx.author.id, ctx=ctx)


@bot.tree.command(name="waterreminder")
async def slash_waterreminder(interaction: discord.Interaction):
    """Subscribe to hourly water reminders."""
    await handle_waterreminder(interaction.user.id, interaction=interaction)


@bot.command()
async def sync(ctx):
    """Sync slash commands with Discord. Owner only."""
    if ctx.author.id != ALLOWED_DM_USER_ID:
        await ctx.send("❌ You don't have permission to use this command.")
        return
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Synced {len(synced)} slash commands with Discord!")
    except Exception as e:
        await ctx.send(f"❌ Failed to sync commands: {e}")


@bot.command()
async def purge(ctx, count: int = 10):
    """Moderator command: bulk-delete `count` messages from the current channel."""
    if not is_mod(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return
    if count < 1 or count > 100:
        await ctx.send("Please specify a count between 1 and 100.")
        return
    try:
        deleted = await ctx.channel.purge(limit=count+1)
        await ctx.send(f"🧹 Purged {len(deleted)-1} messages.", delete_after=5)
    except Exception as e:
        await ctx.send(f"Failed to purge messages: {e}")


@bot.tree.command(name="purge")
@app_commands.describe(count="Number of messages to delete (1-100)")
async def slash_purge(interaction: discord.Interaction, count: int = 10):
    if not is_mod_interaction(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    if count < 1 or count > 100:
        await interaction.response.send_message("Please specify a count between 1 and 100.", ephemeral=True)
        return
    try:
        deleted = await interaction.channel.purge(limit=count+1)
        await interaction.response.send_message(f"🧹 Purged {len(deleted)-1} messages.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to purge messages: {e}", ephemeral=True)


@bot.command()
async def announce(ctx, channel: discord.TextChannel, *, message: str):
    """Moderator command: send a highlighted announcement to a channel."""
    if not is_mod(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return
    try:
        embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.gold())
        embed.set_footer(text=f"Posted by {ctx.author.display_name}")
        await channel.send(embed=embed)
        await ctx.send(f"✅ Announcement sent to {channel.mention}.")
    except Exception as e:
        await ctx.send(f"Failed to send announcement: {e}")


@bot.tree.command(name="announce")
@app_commands.describe(channel="Target channel", message="Announcement message")
async def slash_announce(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    if not is_mod_interaction(interaction):
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    try:
        embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.gold())
        embed.set_footer(text=f"Posted by {interaction.user.display_name}")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Announcement sent to {channel.mention}.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to send announcement: {e}", ephemeral=True)


@bot.command()
async def about(ctx):
    """Show information about Ron Bot."""
    embed = discord.Embed(
        title="🤖 Ron Bot",
        description="The friendly wellness and moderation companion!",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Features",
        value="💧 Hydration Reminders • 💪 Wellness • 🎯 Motivation • 🧹 Moderation",
        inline=False
    )
    embed.add_field(
        name="Commands",
        value="`!quote` • `!roll NdM` • `!ping` • `!remind` • `!waterreminder` • `!purge` • `!announce` • `!stats` • `!leaderboard` • `!health`",
        inline=False
    )
    embed.add_field(
        name="QOL Features",
        value="`!help` • `!motivate` • `!workout` • `!breathing` • `!tip` • `!about`",
        inline=False
    )
    embed.set_footer(text="Stay hydrated, stay healthy! 💚")
    await ctx.send(embed=embed)


@bot.tree.command(name="about")
async def slash_about(interaction: discord.Interaction):
    """Show information about Ron Bot."""
    embed = discord.Embed(
        title="🤖 Ron Bot",
        description="The friendly wellness and moderation companion!",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Features",
        value="💧 Hydration Reminders • 💪 Wellness • 🎯 Motivation • 🧹 Moderation",
        inline=False
    )
    embed.add_field(
        name="Commands",
        value="`/quote` • `/roll` • `/ping` • `/remind` • `/waterreminder` • `/purge` • `/announce` • `/stats` • `/leaderboard` • `/health`",
        inline=False
    )
    embed.add_field(
        name="QOL Features",
        value="`/help` • `/motivate` • `/workout` • `/breathing` • `/tip` • `/about`",
        inline=False
    )
    embed.set_footer(text="Stay hydrated, stay healthy! 💚")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="help")
async def slash_help(interaction: discord.Interaction):
    """Show all available Ron Bot commands."""
    embed = discord.Embed(
        title="📚 Ron Bot Commands",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="🧹 **Moderation**",
        value="`/purge <count>` - Bulk delete messages (mods only)\n`/announce <channel> <message>` - Post an announcement",
        inline=False
    )
    
    embed.add_field(
        name="🎯 **Fun & Motivation**",
        value="`/ping` - Check bot latency\n"
              "`/quote` - Random motivational quote\n"
              "`/motivate` - Quick motivation boost\n"
              "`/roll NdM` - Roll dice (e.g., 2d6, d20)",
        inline=False
    )
    
    embed.add_field(
        name="💚 **Wellness**",
        value="`/waterreminder` - Subscribe to hourly water reminders\n"
              "`/workout` - Get a quick workout suggestion\n"
              "`/breathing` - Guided breathing exercises\n"
              "`/tip` - Daily wellness tip",
        inline=False
    )
    
    embed.add_field(
        name="⏰ **Reminders**",
        value="`/remind <minutes> <message>` - Set a personal reminder",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ **Info**",
        value="`/about` - About Ron Bot\n"
              "`/help` - This message",
        inline=False
    )
    embed.add_field(
        name="📊 **Stats & Health**",
        value="`/stats` - View your reminder stats\n"
              "`/leaderboard` - See top streaks\n"
              "`/health` - Bot status (owner only)",
        inline=False
    )
    
    embed.set_footer(text="Both prefix (!) and slash (/) commands work!")
    await interaction.response.send_message(embed=embed)


@bot.command()
async def motivate(ctx):
    """Get a quick motivational boost."""
    motivations = [
        f"💪 {random.choice(AFFIRMATIONS)}",
    ]
    await ctx.send(random.choice(motivations))


@bot.tree.command(name="motivate")
async def slash_motivate(interaction: discord.Interaction):
    """Get a quick motivational boost."""
    await interaction.response.send_message(f"💪 {random.choice(AFFIRMATIONS)}")


@bot.command()
async def workout(ctx, difficulty: str = None):
    """Get a workout suggestion. Usage: !workout [difficulty]"""
    workouts = {
        "easy": ["10 push-ups", "15 squats", "20 jumping jacks"],
        "medium": ["20 push-ups", "30 squats", "1-minute plank"],
        "hard": ["30 push-ups", "50 squats", "2-minute plank"]
    }

    if difficulty and difficulty.lower() in workouts:
        suggestion = random.choice(workouts[difficulty.lower()])
        await ctx.send(f"💪 {difficulty.capitalize()} workout: {suggestion}")
    else:
        all_workouts = [item for sublist in workouts.values() for item in sublist]
        suggestion = random.choice(all_workouts)
        await ctx.send(f"💪 Random workout: {suggestion}")

@bot.command()
async def tip(ctx, theme: str = None):
    """Get a wellness tip. Usage: !tip [theme]"""
    tips = {
        "hydration": ["Drink a glass of water every hour.", "Carry a reusable water bottle."],
        "mindfulness": ["Take 5 deep breaths.", "Spend 5 minutes meditating."],
        "fitness": ["Stretch for 5 minutes.", "Take a short walk."]
    }

    if theme and theme.lower() in tips:
        suggestion = random.choice(tips[theme.lower()])
        await ctx.send(f"🌟 {theme.capitalize()} tip: {suggestion}")
    else:
        all_tips = [item for sublist in tips.values() for item in sublist]
        suggestion = random.choice(all_tips)
        await ctx.send(f"🌟 Random tip: {suggestion}")


@bot.command()
async def stats(ctx):
    """Show user engagement stats. Usage: !stats"""
    user_id = str(ctx.author.id)
    user_data = reminders.get(user_id, {})

    streak = user_data.get("streak", 0)
    subscribed = "Yes" if user_data.get("subscribed") else "No"

    await ctx.send(
        f"📊 **Your Stats:**\n"
        f"- Subscribed to reminders: {subscribed}\n"
        f"- Current streak: {streak} days"
    )

@bot.command()
async def leaderboard(ctx):
    """Show top users by streak. Usage: !leaderboard"""
    sorted_users = sorted(
        reminders.items(), key=lambda x: x[1].get("streak", 0), reverse=True
    )
    top_users = sorted_users[:10]

    leaderboard = "\n".join(
        [f"{i+1}. <@{user_id}> - {data.get('streak', 0)} days" for i, (user_id, data) in enumerate(top_users)]
    )

    await ctx.send(f"🏆 **Leaderboard:**\n{leaderboard}")


@bot.command()
@commands.is_owner()
async def health(ctx):
    """Check the bot's health and status. Usage: !health"""
    uptime = datetime.now() - bot.launch_time
    active_reminders = len(reminders)

    embed = discord.Embed(title="Bot Health Check", color=0x00ff00)
    embed.add_field(name="Uptime", value=str(uptime).split('.')[0], inline=False)
    embed.add_field(name="Active Reminders", value=str(active_reminders), inline=False)
    embed.add_field(name="Memory Usage", value=f"{psutil.virtual_memory().percent}%", inline=False)

    await ctx.send(embed=embed)

# Track bot launch time
bot.launch_time = datetime.now()


# entrypoint when executed as a script; keeps behaviour consistent with
# prior versions which simply invoked `bot.run()` at module level. Having a
# guard also allows import‑time unit tests or linting without side effects.
if __name__ == "__main__":
    # run() will block until the bot exits; any exception will be logged
    try:
        bot.run(TOKEN)
    except Exception as e:
        logging.error(f"Failed to start Ron Bot: {e}")
        raise
