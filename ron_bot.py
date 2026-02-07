import os
import json
import random
import asyncio
import requests
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "configs.json"

ALLOWED_DM_USER_ID = 821102915325526046

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_PREFIX = os.getenv("PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


def load_configs():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            return {}
    return {}


def save_configs(configs: dict):
    CONFIG_PATH.write_text(json.dumps(configs, indent=2))


configs = load_configs()

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

# Track users who want water reminders
WATER_REMINDER_USERS = set()

AFFIRMATIONS = [
    "You are capable of amazing things. 💪",
    "Your potential is limitless. ✨",
    "You are stronger than you think. 🌟",
    "Your effort matters. Every step counts. 👣",
    "You deserve success and happiness. 🎯",
    "You are making a positive difference. 💖",
    "Progress over perfection. You're doing great! 🚀",
    "Your challenges are opportunities to grow. 🌱",
    "You are resilient and resourceful. 🏆",
    "Today is a fresh start to be your best self. ☀️",
    "You bring value to those around you. 🤝",
    "Your dreams are worth pursuing. 💭",
]

WORKOUT_IDEAS = [
    "⏱️ **2-Minute Desk Stretch**: Stand, reach arms up, lean left, then right. Great for posture!",
    "🏃 **10 Jumping Jacks**: Quick cardio boost to get your blood flowing!",
    "📍 **Wall Push-ups**: Do 10-15 push-ups against a wall. Stronger arms incoming!",
    "🧘 **5-Minute Walk**: Take a quick walk to refresh your mind and body.",
    "💪 **Bodyweight Squats**: 15-20 squats with proper form. Leg strength boost!",
    "🤸 **Plank Hold**: Hold for 30-60 seconds. Core strength is key!",
    "🏃 **Stairs**: Run up and down stairs 5 times. Great cardio!",
    "🙏 **Yoga Flow**: 10 minutes of stretching and light yoga. Flexibility FTW!",
    "👣 **Lunges**: 10 lunges per leg. Powerful leg workout!",
    "⛹️ **High Knees**: Do high knees in place for 30 seconds. Cardio blast!",
]

BREATHING_EXERCISES = [
    "🌬️ **Box Breathing (4-4-4-4)**:\n  1. Breathe in for 4 counts\n  2. Hold for 4 counts\n  3. Breathe out for 4 counts\n  4. Hold for 4 counts\n  Repeat 5 times. Perfect for calmness.",
    "🌊 **4-7-8 Breathing** (Relaxation):\n  1. Breathe in for 4 counts\n  2. Hold for 7 counts\n  3. Breathe out for 8 counts\n  Repeat 5 times. Great for sleep!",
    "🌬️ **Belly Breathing** (Grounding):\n  1. Put hand on belly\n  2. Inhale deeply, feel belly expand\n  3. Exhale slowly, feel belly contract\n  Repeat 10 times. Activates calm.",
    "🎯 **Energizing Breath** (Morning boost):\n  1. Quick short inhales (sniff sniff sniff)\n  2. Long slow exhale\n  Repeat 1 minute. Great for energy!",
]

WELLNESS_TIPS = [
    "💤 Sleep: Aim for 7-9 hours nightly. Your brain and body need recovery time!",
    "💧 Hydration: Drink water throughout the day. A rule: 8 glasses or more!",
    "🚶 Movement: Take a 20-minute walk daily. Great for body and mind.",
    "🍎 Nutrition: Eat whole foods. Your energy levels depend on good nutrition.",
    "🧘 Mindfulness: Spend 5 minutes daily on breathing or meditation.",
    "📱 Digital Detox: Limit screen time 1 hour before bed.",
    "☀️ Sunlight: Get 15-20 minutes of morning sunlight. Boosts mood!",
    "👥 Social: Connect with friends/family. Humans need social connection.",
    "📚 Learning: Learn something new daily. Keeps your brain sharp!",
    "🎵 Music: Listen to uplifting music. Mood booster!",
    "🎯 Goals: Set small achievable goals daily. Momentum builds success!",
    "✍️ Gratitude: Write down 3 things you're grateful for daily.",
]


async def determine_prefix(bot, message):
    return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)


def get_weather_emoji(description: str) -> str:
    """Return emoji based on weather description."""
    desc = description.lower()
    if "clear" in desc or "sunny" in desc:
        return "☀️"
    elif "cloud" in desc:
        return "☁️"
    elif "rain" in desc or "drizzle" in desc:
        return "🌧️"
    elif "thunderstorm" in desc:
        return "⛈️"
    elif "snow" in desc:
        return "❄️"
    elif "wind" in desc:
        return "💨"
    elif "fog" in desc or "mist" in desc:
        return "🌫️"
    else:
        return "🌤️"


async def fetch_weather(city: str) -> dict:
    """Fetch weather data for a city using wttr.in API."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return None


bot = commands.Bot(command_prefix=determine_prefix, intents=intents, description="Ron - The friendly weather and wellness bot")
bot.water_reminder_task = None  # Will be set in on_ready()

# Disable the built-in help command so we can use our custom one
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"Ron is ready. Logged in as: {bot.user} (ID: {bot.user.id})")
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
                    reminders = [
                        "💧 Time to drink some water! Stay hydrated.",
                        "💧 Don't forget to hydrate! Drink a glass of water.",
                        "💧 Hydration check! Have you had enough water today?",
                        "💧 Your body needs water! Take a drink and stretch.",
                        "💧 Feeling thirsty? Drink up! Stay healthy.",
                        "💧 Reminder: Drink water for better focus and health!",
                    ]
                    await user.send(random.choice(reminders))
                except Exception:
                    WATER_REMINDER_USERS.discard(user_id)
        except asyncio.CancelledError:
            break
        except Exception:
            pass


def is_mod(ctx):
    return ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_guild


def is_mod_interaction(interaction: discord.Interaction):
    if not interaction.guild:
        return False
    user = interaction.user
    return user.guild_permissions.administrator or user.guild_permissions.manage_guild


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


@bot.command()
async def weather(ctx, *, city: str):
    """Get the current weather for a city. Usage: !weather London"""
    async with ctx.typing():
        data = await fetch_weather(city)
        if not data or "current_condition" not in str(data):
            await ctx.send(f"❌ Could not find weather data for '{city}'. Please try another city name.")
            return
        
        try:
            current = data["current_condition"][0]
            location = data["nearest_area"][0]
            
            temp_c = current.get("temp_C", "N/A")
            temp_f = current.get("temp_F", "N/A")
            condition = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
            humidity = current.get("humidity", "N/A")
            wind_kph = current.get("windspeedKmph", "N/A")
            feels_like_c = current.get("FeelsLikeC", "N/A")
            
            city_name = location.get("areaName", [{}])[0].get("value", city)
            country = location.get("country", [{}])[0].get("value", "")
            
            emoji = get_weather_emoji(condition)
            
            embed = discord.Embed(
                title=f"{emoji} Weather in {city_name}, {country}",
                description=condition,
                color=discord.Color.blue()
            )
            embed.add_field(name="🌡️ Temperature", value=f"{temp_c}°C ({temp_f}°F)", inline=True)
            embed.add_field(name="🤔 Feels Like", value=f"{feels_like_c}°C", inline=True)
            embed.add_field(name="💨 Wind Speed", value=f"{wind_kph} km/h", inline=True)
            embed.add_field(name="💧 Humidity", value=f"{humidity}%", inline=True)
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error processing weather data: {str(e)}")


@bot.tree.command(name="weather")
@app_commands.describe(city="City name to get weather for")
async def slash_weather(interaction: discord.Interaction, city: str):
    """Get the current weather for a city."""
    await interaction.response.defer()
    data = await fetch_weather(city)
    if not data or "current_condition" not in str(data):
        await interaction.followup.send(f"❌ Could not find weather data for '{city}'. Please try another city name.")
        return
    
    try:
        current = data["current_condition"][0]
        location = data["nearest_area"][0]
        
        temp_c = current.get("temp_C", "N/A")
        temp_f = current.get("temp_F", "N/A")
        condition = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        humidity = current.get("humidity", "N/A")
        wind_kph = current.get("windspeedKmph", "N/A")
        feels_like_c = current.get("FeelsLikeC", "N/A")
        
        city_name = location.get("areaName", [{}])[0].get("value", city)
        country = location.get("country", [{}])[0].get("value", "")
        
        emoji = get_weather_emoji(condition)
        
        embed = discord.Embed(
            title=f"{emoji} Weather in {city_name}, {country}",
            description=condition,
            color=discord.Color.blue()
        )
        embed.add_field(name="🌡️ Temperature", value=f"{temp_c}°C ({temp_f}°F)", inline=True)
        embed.add_field(name="🤔 Feels Like", value=f"{feels_like_c}°C", inline=True)
        embed.add_field(name="💨 Wind Speed", value=f"{wind_kph} km/h", inline=True)
        embed.add_field(name="💧 Humidity", value=f"{humidity}%", inline=True)
        
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Error processing weather data: {str(e)}")


@bot.command()
async def waterreminder(ctx):
    """Subscribe to hourly water reminders. Usage: !waterreminder"""
    user_id = ctx.author.id
    if user_id in WATER_REMINDER_USERS:
        WATER_REMINDER_USERS.discard(user_id)
        await ctx.send("💧 You've unsubscribed from water reminders.")
    else:
        WATER_REMINDER_USERS.add(user_id)
        await ctx.send("💧 You've subscribed to hourly water reminders! Stay hydrated! 💪")


@bot.tree.command(name="waterreminder")
async def slash_waterreminder(interaction: discord.Interaction):
    """Subscribe to hourly water reminders."""
    user_id = interaction.user.id
    if user_id in WATER_REMINDER_USERS:
        WATER_REMINDER_USERS.discard(user_id)
        await interaction.response.send_message("💧 You've unsubscribed from water reminders.")
    else:
        WATER_REMINDER_USERS.add(user_id)
        await interaction.response.send_message("💧 You've subscribed to hourly water reminders! Stay hydrated! 💪")


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
async def about(ctx):
    """Show information about Ron Bot."""
    embed = discord.Embed(
        title="🤖 Ron Bot",
        description="The friendly weather and wellness companion!",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Features",
        value="🌍 Weather • 💧 Hydration Reminders • 💪 Wellness • 🎯 Motivation",
        inline=False
    )
    embed.add_field(
        name="Commands",
        value="`!weather <city>` • `!quote` • `!roll NdM` • `!ping` • `!remind` • `!waterreminder`",
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
        description="The friendly weather and wellness companion!",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Features",
        value="🌍 Weather • 💧 Hydration Reminders • 💪 Wellness • 🎯 Motivation",
        inline=False
    )
    embed.add_field(
        name="Commands",
        value="`/weather` • `/quote` • `/roll` • `/ping` • `/remind` • `/waterreminder`",
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
        name="🌍 **Weather**",
        value="`/weather <city>` - Get current weather for any city with details",
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
async def workout(ctx):
    """Get a quick workout suggestion."""
    suggestion = random.choice(WORKOUT_IDEAS)
    embed = discord.Embed(
        title="💪 Quick Workout Suggestion",
        description=suggestion,
        color=discord.Color.red()
    )
    embed.set_footer(text="Get moving! Your body will thank you! 🏃")
    await ctx.send(embed=embed)


@bot.tree.command(name="workout")
async def slash_workout(interaction: discord.Interaction):
    """Get a quick workout suggestion."""
    suggestion = random.choice(WORKOUT_IDEAS)
    embed = discord.Embed(
        title="💪 Quick Workout Suggestion",
        description=suggestion,
        color=discord.Color.red()
    )
    embed.set_footer(text="Get moving! Your body will thank you! 🏃")
    await interaction.response.send_message(embed=embed)


@bot.command()
async def breathing(ctx):
    """Get a guided breathing exercise."""
    exercise = random.choice(BREATHING_EXERCISES)
    embed = discord.Embed(
        title="🌬️ Breathing Exercise",
        description=exercise,
        color=discord.Color.blurple()
    )
    embed.set_footer(text="Take your time. Breathing is the foundation of calm.")
    await ctx.send(embed=embed)


@bot.tree.command(name="breathing")
async def slash_breathing(interaction: discord.Interaction):
    """Get a guided breathing exercise."""
    exercise = random.choice(BREATHING_EXERCISES)
    embed = discord.Embed(
        title="🌬️ Breathing Exercise",
        description=exercise,
        color=discord.Color.blurple()
    )
    embed.set_footer(text="Take your time. Breathing is the foundation of calm.")
    await interaction.response.send_message(embed=embed)


@bot.command()
async def tip(ctx):
    """Get a daily wellness tip."""
    wellness_tip = random.choice(WELLNESS_TIPS)
    embed = discord.Embed(
        title="💚 Daily Wellness Tip",
        description=wellness_tip,
        color=discord.Color.green()
    )
    embed.set_footer(text="Small changes lead to big health improvements!")
    await ctx.send(embed=embed)


@bot.tree.command(name="tip")
async def slash_tip(interaction: discord.Interaction):
    """Get a daily wellness tip."""
    wellness_tip = random.choice(WELLNESS_TIPS)
    embed = discord.Embed(
        title="💚 Daily Wellness Tip",
        description=wellness_tip,
        color=discord.Color.green()
    )
    embed.set_footer(text="Small changes lead to big health improvements!")
    await interaction.response.send_message(embed=embed)




if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN not set — create a .env with DISCORD_TOKEN and run again.")
        raise SystemExit(1)
    bot.run(TOKEN)
