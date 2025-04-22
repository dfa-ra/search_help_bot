from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common import CompletableRequestsResult
from core.dao import RequestDao
from core.services.requests_service.draw_request_service import DrawRequestService


class ShowAllOpenRequestsService:

    @inject
    async def execute(
            self
    ) -> CompletableRequestsResult:
        async with DaoContainer.session() as session:
            requests_dao = RequestDao(session)
            request = await requests_dao.get_all_open_requests()
            if request is not []:
                print(request)
                return CompletableRequestsResult.ok(list=request)
            else:
                text = f"Нету открытых заявок"
                return CompletableRequestsResult.fail(Exception(), text)