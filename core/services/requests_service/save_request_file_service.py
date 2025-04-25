from dependency_injector.wiring import Provide, inject

from app.dao_container import DaoContainer
from core.common.completable import CompletableRequestsResult
from core.common.decorators import close_dao_sessions
from core.dao import MongoDao, RequestDao
from telegram import Update
from telegram.ext import ContextTypes

from core.models import FileModel


class SaveRequestFileService:
    @inject
    @close_dao_sessions
    async def execute(
            self,
            id: int,
            telegram_id: int,
            document: FileModel,
            mongo_dao: MongoDao = Provide[DaoContainer.mongo_dao],
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableRequestsResult:

        try:
            mime_type = document.mime_type
            file_name = document.file_name
            file_bytes = document.file_bytes

            print(f"File: {file_name}, Mime type: {mime_type}, File size: {len(file_bytes)} bytes")


            file_id = await mongo_dao.save_file(file_name, mime_type, file_bytes)
            result = await requests_dao.add_file_id_for_requests(id, telegram_id, file_id)
            if result is None:
                return CompletableRequestsResult.fail(error=Exception(), message="Что-то пошло не так")
            return CompletableRequestsResult.ok()
        except Exception as e:
            print(str(e))
            return CompletableRequestsResult.fail(error=e, message="Ошибка сохранения файла... заявка не сохранена :( ")
