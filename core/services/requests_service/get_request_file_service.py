from dependency_injector.wiring import Provide, inject

from app.dao_container import DaoContainer
from core.common.completable import CompletableFileResult
from core.common.decorators import close_dao_sessions
from core.dao import MongoDao, RequestDao
from core.models import FileModel,  Request


class GetRequestFileByIdService:
    @inject
    @close_dao_sessions
    async def execute(
            self,
            id: int,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
            mongo_dao: MongoDao = Provide[DaoContainer.mongo_dao]
    ) -> CompletableFileResult:
        try:
            result = await requests_dao.get_request_file_id(id)
            print(f"1 этап пройден: {result.id}")
            file_result: FileModel = await mongo_dao.get_file(result.file_id)
            print("2 этап пройден")
            return CompletableFileResult.ok(file=file_result)
        except Exception as e:
            return CompletableFileResult.fail(error=e, message=str(e))

