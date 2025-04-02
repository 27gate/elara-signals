import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db import init_db, add_user

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # ← безопасно!

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    await update.message.reply_text(
        f"👁 Привет, {user.first_name}.\nТы подключился к Elara.\nВведи свою дату рождения (в формате ДД.ММ.ГГГГ), чтобы получить первый знак."
    )

def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()

from telegram.ext import MessageHandler, filters
from datetime import datetime
from db import update_birthdate  # мы сейчас допишем эту функцию

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text.strip()

    # Пробуем распознать дату
    try:
        birthdate = datetime.strptime(message, "%d.%m.%Y").date()
        update_birthdate(user.id, birthdate.isoformat())
        await update.message.reply_text(
            f"🗓 Записала твою дату: {birthdate.strftime('%d.%m.%Y')}.\nElara услышала. Завтра ты получишь свой первый знак."
        )
    except ValueError:
        await update.message.reply_text("😶 Я не поняла... Попробуй ввести дату в формате ДД.ММ.ГГГГ.")

