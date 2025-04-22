from dependency_injector.wiring import inject, Provide
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, ContextTypes

from app.service_container import ServiceContainer
from core.models import User
from core.services import AddInfoService

UNIVERSITY, COURSE, DIRECTION = range(3)

async def add_information_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["user"] = User()

    keyboard = [["ИТМО", "Политех", "СПБГУ"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Ура, расскажешь о себе! \n\nГде ты учишься?",
        reply_markup=reply_markup
    )

    return UNIVERSITY


async def add_university_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["user"].university = update.message.text

    keyboard = [["1", "2", "3", "4"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("На каком ты курсе?", reply_markup=reply_markup)
    return COURSE


async def add_course_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["user"].course = int(update.message.text)

    await update.message.reply_text("Какое у тебя направление?", reply_markup=ReplyKeyboardRemove())
    return DIRECTION


@inject
async def add_direction_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    add_info_user: AddInfoService = Provide[ServiceContainer.add_info_user],
):
    context.user_data["user"].direction = update.message.text

    user = context.user_data["user"]

    result = await add_info_user.execute(
        telegram_id=update.effective_user.id,
        university=user.university,
        course=user.course,
        direction=user.direction,
    )

    await update.message.reply_text(f"{result.message}")
    del context.user_data["user"]
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Окей, отменено", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END