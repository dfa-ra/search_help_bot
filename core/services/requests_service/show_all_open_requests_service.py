from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common.completable import CompletableRequestsResult
from core.common.decorators import close_dao_sessions
from core.dao import RequestDao
from core.services.requests_service.draw_request_service import DrawRequestService


class ShowAllOpenRequestsService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            telegram_id: int,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableRequestsResult:
        request = await requests_dao.get_all_open_requests(telegram_id)
        if request is not []:
            print(request)
            return CompletableRequestsResult.ok(list=request)
        else:
            text = f"Нету открытых заявок"
            return CompletableRequestsResult.fail(Exception(), text)