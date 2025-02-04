import os
import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi dari Environment Variables
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Jakarta")
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "16:30")  # Format: HH:MM

intents = discord.Intents.default()
intents.members = True  # 
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot is online! Ready to remind the team to fill daily log.")
    
    # Parse waktu dari environment variable
    hour, minute = map(int, SCHEDULE_TIME.split(':'))
    
    # Setup scheduler
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        create_thread,
        "cron",
        day_of_week="mon-fri",
        hour=hour,
        minute=minute
    )
    scheduler.start()
    print(f"Scheduled activated!")

async def create_thread():
    channel = bot.get_channel(CHANNEL_ID)
    role = channel.guild.get_role(ROLE_ID)
    
    # Validasi environment variables
    if not channel or not role:
        print("ERROR: Channel or Role cannot be found. Please check the environment variables!")
        return
    
    try:
        # Buat thread di forum/text channel
        if isinstance(channel, discord.ForumChannel):
            thread = await channel.create_thread(
                name=f"Log {datetime.now().strftime('%A, %-d %b %Y')}",
                content=f"{role.mention} Please fill the daily log here!",
                auto_archive_duration=1440
            )
        else:
            message = await channel.send(f"🔔 Hi{role.mention}! Don't forget to fill in your Daily Log for today!")
            thread = await message.create_thread(name=f"Log {datetime.now().strftime('%A, %-d %b %Y')}")
        
        await thread.send("📋 **Format:**\n- Done\n- In progress\n- Not Started\n> Or you can [generate here](https://notion-standup-generator-xom75utdta-as.a.run.app/)")
        print(f"Thread {thread.name} already created!")
    except Exception as e:
        print(f"Failed to create thread: {str(e)}")

if __name__ == "__main__":
    bot.run(TOKEN)