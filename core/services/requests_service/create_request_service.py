from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common.completable import SingleResult
from core.common.custom_errors import ErrorTypes
from core.common.decorators import close_dao_sessions
from core.dao import RequestDao
from core.models import RequestModel


class CreateRequestService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            request: RequestModel,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> SingleResult:
        try:
            result: RequestModel = await requests_dao.create_request(request)
            return SingleResult.ok("\/ Заявка успешно создана", result=result)
        except Exception as e:
            return SingleResult.fail(e, message="слишком большое число", error_type=ErrorTypes.NOT_INT_32_ERROR)
