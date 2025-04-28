from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, ContextTypes


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" # Окей, отменено", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
