import os
import re
import requests
import instaloader
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8757705485:AAGC2YKFu7QO40vRWnqRndBZI3sZsRq8_Aw")

L = instaloader.Instaloader(
    download_pictures=False,
    download_comments=False,
    save_metadata=False
)

def extract_shortcode(url):
    match = re.search(r"(?:reel|p|tv)/([^/?&]+)", url)
    return match.group(1) if match else None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com" not in text:
        await update.message.reply_text("❌ Send a valid Instagram link.")
        return

    shortcode = extract_shortcode(text)

    if not shortcode:
        await update.message.reply_text("❌ Invalid Instagram URL.")
        return

    await update.message.reply_text("⬇️ Downloading... Please wait")

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if not post.is_video:
            await update.message.reply_text("⚠️ This post is not a video.")
            return

        video_url = post.video_url

        file_name = f"{shortcode}.mp4"

        r = requests.get(video_url, stream=True, timeout=10)

        with open(file_name, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        await update.message.reply_video(video=open(file_name, "rb"))

        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("🚀 Bot is running...")
app.run_polling()