import discord
import os
from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AUTHORIZED_USER_IDS = [
    int(uid.strip())
    for uid in os.getenv("DISCORD_AUTHORIZED_USER_IDS", "").split(",")
    if uid.strip()
]

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Tally Agent is online as {client.user}")

@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return

    # Only respond in #collections-bot channel
    if message.channel.name != "collections-bot":
        return

    # Auth check — drop unauthorized users silently
    if message.author.id not in AUTHORIZED_USER_IDS:
        print(f"⛔ Unauthorized user: {message.author.id}")
        return

    # Show typing indicator while agent processes
    async with message.channel.typing():
        print(f"📩 Message from {message.author}: {message.content}")
        response = run_agent(message.content)

    # Discord has a 2000 char limit — split if needed
    if len(response) <= 2000:
        await message.channel.send(response)
    else:
        chunks = [response[i:i+1990] for i in range(0, len(response), 1990)]
        for chunk in chunks:
            await message.channel.send(chunk)

# --- Start Bot ---
if __name__ == "__main__":
    print("🚀 Starting Tally Agent...")
    client.run(DISCORD_BOT_TOKEN)