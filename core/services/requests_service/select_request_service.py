from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common.completable import CompletableRequestsResult
from core.common.decorators import close_dao_sessions
from core.dao import RequestDao


class SelectRequestService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            id: int,
            telegram_id: int,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableRequestsResult:
        count = await requests_dao.count_executor_requests(telegram_id)
        if count > 2:
            return CompletableRequestsResult.ok(f"!! Вы и так выполняете уже более 2 заявок")
        try:
            result = await requests_dao.add_executor_for_requests(id, telegram_id)
            if result is not None:
                return CompletableRequestsResult.ok(f"\/ Заявка №{id} закреплена за вами")
            else:
                return CompletableRequestsResult.ok(
                    f"!! Данная заявка №{id} не может быть закреплена за вами так как она либо в работе либо является вашей заявкой")
        except Exception as e:
            return CompletableRequestsResult.fail(e, f"!! Не закрепить за вами заявку №{id}")
