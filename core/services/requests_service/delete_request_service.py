from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.dao import RequestDao


class DeleteRequestService:

    @inject
    async def execute(
            self,
            id: int,
            telegram_id: int,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableResult:
        try:
            result: bool = await requests_dao.delete_requests(id, telegram_id)
            if result:
                return CompletableResult.ok(f"\/ Заявка №{id} успешно удалена")
            else:
                return CompletableResult.ok(f"!! Заявку №{id} удалить не получилоось, возможно вы не являетесь создателем этой заявки")
        except Exception as e:
            return CompletableResult.fail(e, "!! Произошла ошибка при удалении заявки")
