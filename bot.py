import re
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from downloader import get_video_url, load_session
from rate_limiter import is_allowed
from cache import get_cache_path, is_cached
from worker import queue, worker

BOT_TOKEN = os.getenv("BOT_TOKEN")

def extract_shortcode(url):
    match = re.search(r"(?:reel|p|tv)/([^/?&]+)", url)
    return match.group(1) if match else None

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if not is_allowed(user_id):
        await update.message.reply_text("⏳ Slow down a bit!")
        return

    if "instagram.com" not in text:
        await update.message.reply_text("❌ Send valid Instagram link")
        return

    shortcode = extract_shortcode(text)

    if not shortcode:
        await update.message.reply_text("❌ Invalid URL")
        return

    await update.message.reply_text("⬇️ Processing...")

    video_url = get_video_url(shortcode, text)

    if not video_url:
        await update.message.reply_text("⚠️ Failed to fetch video")
        return

    file_path = get_cache_path(video_url)

    if not is_cached(video_url):
        await queue.put((video_url, file_path))
        await asyncio.sleep(2)

    await update.message.reply_video(video=open(file_path, "rb"))

async def main():
    load_session()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle))

    asyncio.create_task(worker())

    print("🚀 Advanced bot running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
