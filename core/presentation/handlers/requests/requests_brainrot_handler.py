from dependency_injector.wiring import inject, Provide
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from app.service_container import ServiceContainer
from core.common.completable import CompletableRequestsResult, CompletableFileResult
from core.services import ShowAllOpenRequestsService, DrawRequestService, SelectRequestService, \
    GetRequestFileByIdService

user_sessions = {}

def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["✅ Взять", "⛔ Закончить", "➡️ Далее"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


@inject
async def requests_brainrot_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        get_request_file_service: GetRequestFileByIdService = Provide[ServiceContainer.get_request_file_service],
        show_all_open_requests_service: ShowAllOpenRequestsService = Provide[ServiceContainer.show_all_open_requests_service],
        draw_request_service: DrawRequestService = Provide[ServiceContainer.draw_request_service],
):
    requests: CompletableRequestsResult = await show_all_open_requests_service.execute(update.effective_user.id)
    if requests.is_success():
        print(requests)
        if not (requests.list == []):
            user_id = update.effective_user.id
            context.user_data["brainrot"] = True
            user_sessions[user_id] = {
                "start": True,
                "list": requests.list,
                "index": 0
            }
            index = 0
            result = await draw_request_service.execute(requests.list[index])
            file_result: CompletableFileResult = await get_request_file_service.execute(requests.list[index].id)
            await update.message.reply_document(
                document=file_result.file.file_bytes,
                filename=file_result.file.file_name,
                caption=result,
                reply_markup=get_keyboard()
            )
    else:
        await update.message.reply_text(requests.message)

@inject
async def request_brainrot_button_handle(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        select_request_service: SelectRequestService = Provide[ServiceContainer.select_request_service],
        draw_request_service: DrawRequestService = Provide[ServiceContainer.draw_request_service],
):
    if "brainrot" not in context.user_data:
        return
    message = update.message
    user_id = message.from_user.id
    choice = message.text.strip()

    session = user_sessions.get(user_id)
    if not session:
        await message.reply_text("Ты не начинал сессию. Напиши команду сначала.")
        return

    list_request = session["list"]
    index = session["index"]

    if choice == "✅ Взять":
        result = await select_request_service.execute(list_request[index].id, user_id)
        await message.reply_text(result.message)

    elif choice == "⛔ Закончить":
        await message.reply_text("Согл и так чёт дофига всего на тебя взвалили!", reply_markup=None)
        user_sessions.pop(user_id, None)
        return

    elif choice != "➡️ Далее":
        await message.reply_text("Выбери один из предложенных вариантов кнопками 👇")
        return

    index += 1
    if index >= len(list_request):
        await message.reply_text("Все заявки просмотрены. Заходи позже!", reply_markup=None)
        user_sessions.pop(user_id, None)
        return

    session["index"] = index
    result = await draw_request_service.execute(list_request[index])
    del context.user_data["brainrot"]
    await message.reply_text(result, reply_markup=get_keyboard())
