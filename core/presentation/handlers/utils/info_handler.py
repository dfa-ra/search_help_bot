from telegram import Update
from telegram.ext import ContextTypes


async def info_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
):
    text = (f"Мои пальцы — пистолеты\n"
            f"Пау-пау-пау-пау-пау (Вух)\n"
            f"Я стреляю сигареты, раздаю бомжам\n"
            f"Я ещё совсем малышка, мелюзга\n"
            f"На моих зубах железки, больно целовать\n"
            f"Школа не нужна, школа не нужна-на-на\n"
            f"Школа не нужна, школа не нужна-а-а-а")

    await update.message.reply_text(text)
