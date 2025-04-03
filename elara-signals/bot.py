import logging
import os
import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from db import init_db, add_user, update_birthdate
from forecast import generate_forecast  # генератор прогноза через GPT

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        f"👁 Привет, {user.first_name}.
"
        "Ты подключился к Elara.
"
        "Введи свою дату рождения (в формате ДД.ММ.ГГГГ), чтобы получить первый знак."
    )

# Обработка обычного текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text.strip()

    try:
        birthdate = datetime.strptime(message, "%d.%m.%Y").date()
        update_birthdate(user.id, birthdate.isoformat())
        await update.message.reply_text(
            f"🗓 Записала твою дату: {birthdate.strftime('%d.%m.%Y')}.
"
            "Elara услышала. Сейчас она настроится…"
        )

        await update.message.reply_text("🔮 Чувствую твой ритм... Слушаю Знаки...")

        forecast = generate_forecast(birthdate.strftime('%d.%m.%Y'))
        await update.message.reply_text(forecast)

    except ValueError:
        await update.message.reply_text("😶 Я не поняла... Попробуй ввести дату в формате ДД.ММ.ГГГГ.")

def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
