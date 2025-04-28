from dependency_injector.wiring import Provide, inject

from app.dao_container import DaoContainer
from core.common.completable import CompletableResult
from core.common.decorators import close_dao_sessions
from core.dao import MongoDao, RequestDao

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
    ) -> CompletableResult:

        try:

            print(f"File: {document.file_name}, Mime type: {document.mime_type}, File size: {len(document.file_bytes)} bytes")

            file_id = await mongo_dao.save_file(document)
            result = await requests_dao.add_file_id_for_requests(id, telegram_id, file_id)
            if result is None:
                return CompletableResult.fail(error=Exception(), message="Что-то пошло не так")
            return CompletableResult.ok()
        except Exception as e:
            print(str(e))
            return CompletableResult.fail(error=e, message="Ошибка сохранения файла... заявка не сохранена :( ")
