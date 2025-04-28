from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common.completable import SingleResult
from core.common.decorators import close_dao_sessions
from core.dao import RequestDao


class ShowMyRequestsService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            telegram_id: int,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> SingleResult:
        request = await requests_dao.get_request_by_creator_id(telegram_id)
        if request is not []:
            print(request)
            return SingleResult.ok(result=request)
        else:
            text = f"Нету ваших заявок"
            return SingleResult.fail(error=Exception(), message=text)
