from flask import Flask
import os
import asyncio
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)

# Fetch variables securely from your Render Environment panel
API_ID = int(os.environ.get("TELEGRAM_API_ID", 0))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
MOVIE_CHANNEL_ID = os.environ.get("MOVIE_CHANNEL_ID")

# Initialize the Pyrogram Bot Client
bot = Client(
    "movie_search_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.route('/')
def home():
    return "Scene Movie HD Live Search Engine Running Successfully!"

@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text(
        text=f"Welcome {message.from_user.mention}! 👋\n\n🔍 Send me any movie name (Tamil, Malayalam, Telugu), and I will instantly search our database for the download links!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Search Movies 🔍", switch_inline_query_current_chat="")]
        ])
    )

@bot.on_message(filters.text & ~filters.command(["start"]))
async def search_movies(client: Client, message: Message):
    query = message.text.lower().strip()
    await message.reply_chat_action("typing")
    
    if not MOVIE_CHANNEL_ID:
        response_text = (
            f"🎬 **Search Results for:** `{message.text}`\n\n"
            f"📥 **[Download Server 1]** {message.text} HD Tamil\n"
            "⚠️ *Tip: Link your MOVIE_CHANNEL_ID variable in Render settings.*"
        )
        await message.reply_text(response_text)
        return

    found_files = False
    try:
        async for msg in client.search_messages(chat_id=int(MOVIE_CHANNEL_ID), query=query):
            found_files = True
            await msg.copy(chat_id=message.chat.id)
    except Exception as e:
        print(f"Search system error: {e}")
        
    if not found_files:
        await message.reply_text(f"❌ Sorry, no results found for **{message.text}**.")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot.run()

if __name__ == '__main__':
    if API_ID and API_HASH and BOT_TOKEN:
        bot_thread = Thread(target=run_bot, daemon=True)
        bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
