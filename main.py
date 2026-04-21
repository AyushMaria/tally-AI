import threading
from discord_bot import run_discord
# from whatsapp_bot import run_whatsapp

if __name__ == "__main__":
    print("🚀 Starting Tally Agent...")

    # Run WhatsApp webhook in a background thread
    # wa_thread = threading.Thread(target=run_whatsapp, daemon=True)
    # wa_thread.start()
    # print("✅ WhatsApp webhook running on port 5000")

    # Run Discord bot on the main thread (it manages its own asyncio loop)
    run_discord()