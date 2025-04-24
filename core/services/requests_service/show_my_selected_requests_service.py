from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common import CompletableRequestsResult
from core.dao import RequestDao
from core.services.requests_service.draw_request_service import DrawRequestService


class ShowMySelectedRequestsService:

    @inject
    async def execute(
            self,
            telegram_id: int,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableRequestsResult:
        request = await requests_dao.get_request_by_executor_id(telegram_id)
        if request is not []:
            print(request)
            return CompletableRequestsResult.ok(list=request)
        else:
            text = f"Нету ваших заявок"
            return CompletableRequestsResult.fail(Exception(), text)