from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common import CompletableRequestsResult
from core.dao import RequestDao
from core.services.requests_service.draw_request_service import DrawRequestService


class ShowMyRequestsService:

    @inject
    async def execute(
            self,
            telegram_id: int
    ) -> CompletableRequestsResult:
        async with DaoContainer.session() as session:
            requests_dao = RequestDao(session)
            request = await requests_dao.get_request_by_creator_id(telegram_id)
            if request is not []:
                print(request)
                return CompletableRequestsResult.ok(list=request)
            else:
                text = f"Нету ваших заявок"
                return CompletableRequestsResult.fail(Exception(), text)