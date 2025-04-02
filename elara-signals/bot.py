import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db import init_db, add_user

import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # ← сюда вставь свой токен

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
    app.run_polling()

if __name__ == "__main__":
    main()
