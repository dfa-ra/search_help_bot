from dependency_injector.wiring import Provide

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.dao import MongoDAO, RequestDao
from core.models import Request
from telegram import Update
from telegram.ext import ContextTypes


class SaveRequestFileService:
    async def execute(
            self,
            id: int,
            telegram_id: int,
            context: ContextTypes.DEFAULT_TYPE,
            file: Update.message.document,
            mongo_dao: MongoDAO = Provide[DaoContainer.mongo_dao],
            request_dao: RequestDao = Provide[DaoContainer.request_dao],
    ) -> CompletableResult:
        if file is None:
            return CompletableResult.fail(message="Пожалуйста, пришли файл.")

        telegram_file = await context.bot.get_file(file.file_id)
        file_bytes = await telegram_file.download_as_bytearray()

        try:
            file_id = mongo_dao.save_file(file.file_name, file.mime_type, file_bytes)
            result = request_dao.add_file_id_for_requests(id, telegram_id, file_id)
            if result is None:
                return CompletableResult.fail(message="Что-то пошло не так")
            return CompletableResult.ok()
        except Exception as e:
            return CompletableResult.fail(message=str(e))

