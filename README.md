# Discord Daily Thread Bot 🤖

An automated Discord bot to create daily threads on weekdays (Monday-Friday) at specified times. Threads will automatically tag a designated role and provide a report template.

## Features ✨
- Automated daily thread creation in specified channels.
- Role tagging functionality.
- Predefined report templates.
- Docker support for easy deployment.
- Configuration via environment variables.

## Prerequisites 📋
- Python 3.11+
- [Docker](https://www.docker.com/) (optional)
- Discord bot token from [Developer Portal](https://discord.com/developers/applications)
- Required bot permissions:
  - `Manage Threads`
  - `Send Messages`
  - `Mention @everyone/@roles`

## Installation 🛠️

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/discord-daily-thread.git
cd discord-daily-thread
```

### 2. Setup Environment
```bash
# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
1. Create environtment
```bash
cp .env.example .env
```
2. Edit .env
```bash
DISCORD_TOKEN=your_bot_token_here
CHANNEL_ID=your_channel_id_here
ROLE_ID=your_role_id_here
TIMEZONE=Asia/Jakarta
SCHEDULE_TIME=16:30
```
### 4. Enable Intent
In [Discord Developer Portal](https://discord.com/developers/applications):
1. Go to your bot's page → Bot
2. Enable:
- PRESENCE INTENT
- SERVER MEMBERS INTENT
- MESSAGE CONTENT INTENT (optional)

## Usage 🚀
### Run Without Docker
```bash
python src/bot.py
```

### Run with Docker
1. Build image
```bash
docker build -t discord-daily-thread .
```
2. Run container:
```bash
docker run -d \
  --env-file .env \
  --restart unless-stopped \
  --name daily-thread-bot \
  discord-daily-thread
```
