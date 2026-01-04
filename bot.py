import random
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8573534227:AAEN4-SfbqohLk-Fd-Wbs7_8T95HQp1m-Wk"
CHAT_ID = -5084894998

PORT = 8000
BASE_URL = "https://<ТВОЙ-ПРОЕКТ>.up.railway.app"  # Railway подставит автоматически

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

# ================== ФРАЗЫ ==================
PHOTO_REPLIES = [
    "📸 Вот это кадр!",
    "🖼 Такое в музей надо",
    "😂 Картинка сказала всё",
    "👀 Интересно, интересно…",
    "🎨 Художник внутри тебя жив",
    "😏 Это точно без фотошопа?",
    "📷 Скрин принят",
    "🔥 Контент подъехал",
    "🤔 И как это комментировать?",
    "🤣 Чат оживился",
    "😎 Неплохо, неплохо",
    "🫠 Я не был к этому готов",
    "📸 Сильное фото",
    "👁‍🗨 Есть над чем подумать",
    "😂 Ну всё, пошло-поехало",
    "🖼 Сохраняю в историю",
    "🤨 А что тут происходит?",
    "📷 Вот это момент",
    "😄 Красиво сыграно",
    "🔥 Одобряю",
]

VIDEO_REPLIES = [
    "🎬 Ну всё, залипли",
    "📹 Сейчас будет интересно",
    "😂 Видео решает",
    "👀 Смотрим внимательно",
    "🍿 Где попкорн?",
    "🎥 Классика жанра",
    "😅 Это было неожиданно",
    "🔥 Контент уровня PRO",
    "🤣 Вот это поворот",
    "🎞 Почти кино",
    "😎 Неплохой монтаж",
    "🤯 Что я только что увидел?",
    "📺 Продолжаем смотреть",
    "😂 Ну ты даёшь",
    "🎬 Сюжет закручивается",
    "👁‍🗨 Это надо пересмотреть",
    "🔥 Хорош!",
    "😄 Чат оценил",
    "📹 Сохраню на потом",
    "🫣 Смело",
]

SILENCE_MESSAGES = [
    "🤔 Что-то в группе тишина…",
    "😴 Такое чувство, что все ушли за кофе",
    "📉 Давненько не было смешного контента",
    "👀 Народ, вы где?",
    "😂 Чат скучает по мемам",
    "🫠 Неловкая пауза…",
    "📢 Алё, приём!",
    "😎 Может, кто-нибудь пошутит?",
]

# ================== ОБРАБОТЧИКИ ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Я на месте. Слежу за контентом 👀")

async def on_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.6:
        await update.message.reply_text(random.choice(PHOTO_REPLIES))

async def on_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.6:
        await update.message.reply_text(random.choice(VIDEO_REPLIES))

# ================== ПЕРИОДИЧЕСКИЕ ЗАДАЧИ ==================
async def send_silence_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=random.choice(SILENCE_MESSAGES)
    )

async def send_time_message(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(MOSCOW_TZ)
    text = now.strftime("🕒 Москва: %d.%m.%Y — %H:%M")
    await context.bot.send_message(chat_id=CHAT_ID, text=text)

# ================== MAIN ==================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, on_photo))
    app.add_handler(MessageHandler(filters.VIDEO, on_video))

    job_queue = app.job_queue
    job_queue.run_repeating(send_silence_message, interval=1800, first=1800)
    job_queue.run_repeating(send_time_message, interval=3600, first=3600)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{BASE_URL}/{BOT_TOKEN}",
    )

if __name__ == "__main__":
    main()
