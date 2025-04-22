from telegram import Update
from telegram.ext import ContextTypes


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    str = (f"Привет {update.effective_user.first_name}\n"
           f"Этот бот — настоящий прорыв в автоматизации! Он мгновенно обрабатывает запросы, умно фильтрует данные и работает без единой ошибки. С таким помощником любая задача становится в разы проще и приятнее!")
    await update.message.reply_text(str)


