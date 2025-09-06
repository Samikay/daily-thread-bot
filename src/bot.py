import os
import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Jakarta")
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "16:30")  # Format: HH:MM
LINK = os.getenv("LINK")

intents = discord.Intents.default()
intents.members = True  # 
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot is online! Ready to create daily threads")
    
    # Parse waktu dari environment variable
    hour, minute = map(int, SCHEDULE_TIME.split(':'))
    
    # Setup scheduler
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        create_thread,
        "cron",
        hour=hour,
        minute=minute
    )
    scheduler.start()
    # Testing
    #print(f"Attempting immediate thread creation...")
    #await create_thread()
    print(f"Scheduler activated!")


async def create_thread():
    channel = bot.get_channel(CHANNEL_ID)

    # Validate
    if not channel:
        print("ERROR: Channel cannot be found. Please check the environment variables!")
        return

    try:
        # Thread name = dd/mm/yy
        thread_name = datetime.now().strftime("%d/%m/%y")

        if isinstance(channel, discord.ForumChannel):
            thread = await channel.create_thread(
                name=thread_name,
                content="🏌️ Daily golf time! Let's play: https://kindahardgolf.com/"
            )
        else:
            message = await channel.send("🏌️ Daily golf time " + thread_name + " <https://kindahardgolf.com/>")
            thread = await message.create_thread(name=thread_name)

        print(f"Thread '{thread.name}' created successfully!")
    except Exception as e:
        print(f"Error while creating thread: {e}")

if __name__ == "__main__":
    bot.run(TOKEN)
