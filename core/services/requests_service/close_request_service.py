from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common.completable import CompletableRequestsResult
from core.common.decorators import close_dao_sessions
from core.dao import RequestDao



class CloseRequestService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            id: int,
            telegram_id: int,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableRequestsResult:
        try:
            result: bool = await requests_dao.close_requests(id, telegram_id)
            if result:
                return CompletableRequestsResult.ok(f"\/ Заявка №{id} успешно закрыта")
            else:
                return CompletableRequestsResult.ok(f"!! Заявку №{id} закрыть не получилоось, возможно вы не являетесь создателем этой заявки")
        except Exception as e:
            return CompletableRequestsResult.fail(e, "!! Произошла ошибка при закрытии заявки")
