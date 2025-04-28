from io import BytesIO

from dependency_injector.wiring import inject, Provide
from telegram import Update, ReplyKeyboardMarkup, InputFile, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.common.completable import SingleResult
from core.services import ShowAllOpenRequestsService, DrawRequestService, SelectRequestService, \
    GetRequestFileByIdService
from core.presentation.senders import *

user_sessions = {}


def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["✅ Взять", "⛔ Закончить", "➡️ Далее"]
        ],
        resize_keyboard=True
    )


# хендлер команды /requests_brainrot
# позволяет просматривать заявки как ленту новостей :)
@inject
async def requests_brainrot_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        get_request_file_service: GetRequestFileByIdService = Provide[ServiceContainer.get_request_file_service],
        show_all_open_requests_service: ShowAllOpenRequestsService = Provide[
            ServiceContainer.show_all_open_requests_service],
):
    requests: SingleResult = await show_all_open_requests_service.execute(update.effective_user.id)
    if requests.is_success():
        print(requests)
        if not (requests.result == []):
            user_id = update.effective_user.id
            context.user_data["brainrot"] = True
            user_sessions[user_id] = {
                "start": True,
                "list": requests.result,
                "index": 0
            }
            index = 0
            file_result: SingleResult = await get_request_file_service.execute(requests.result[index].id)
            if file_result.is_success():
                await request_with_file_sender(update, requests.result[index], file_result.result)
            else:
                await request_sender(update, requests.result[index])

            await update.message.reply_text(
                "Выбирай что ты хочешь с ней сделать?",
                reply_markup=get_keyboard()
            )


    else:
        await update.message.reply_text(requests.message)


@inject
async def request_brainrot_button_handle(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        get_request_file_service: GetRequestFileByIdService = Provide[ServiceContainer.get_request_file_service],
        select_request_service: SelectRequestService = Provide[ServiceContainer.select_request_service],
):
    if "brainrot" not in context.user_data:
        return
    message = update.message
    user_id = message.from_user.id
    choice = message.text.strip()

    session = user_sessions.get(user_id)
    if not session:
        await message.reply_text("!! Ты не начинал сессию. Напиши команду сначала.")
        return

    list_request = session["list"]
    index = session["index"]

    if choice == "✅ Взять" or choice == "Взять":
        result = await select_request_service.execute(list_request[index].id, user_id)
        await message.reply_text(result.message)

    elif choice == "⛔ Закончить" or choice == "Закончить":
        del context.user_data["brainrot"]
        await message.reply_text(" # Согл и так чёт дофига всего на тебя взвалили!", reply_markup=ReplyKeyboardRemove())
        user_sessions.pop(user_id, None)
        return

    elif choice != "➡️ Далее" and choice != "Далее":
        await message.reply_text(
            " # Выбери один из предложенных вариантов (Взять/Закончить/Далее) кнопками 👇",
            reply_markup=get_keyboard()
            )
        return

    index += 1
    if index >= len(list_request):
        await message.reply_text(" # Все заявки просмотрены. Заходи позже!", reply_markup=None)
        user_sessions.pop(user_id, None)
        return

    session["index"] = index

    file_result: SingleResult = await get_request_file_service.execute(list_request[index].id)

    if file_result.is_success():
        await request_with_file_sender(update, list_request[index], file_result.result)
    else:
        await request_sender(update, list_request[index])
