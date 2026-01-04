import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))
BASE_URL = os.getenv("RAILWAY_STATIC_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот работает. Webhook активен.")

def main():
    if not BOT_TOKEN or not BASE_URL:
        raise RuntimeError("Нет BOT_TOKEN или RAILWAY_STATIC_URL")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{BASE_URL}/{BOT_TOKEN}",
    )

if __name__ == "__main__":
    main()
