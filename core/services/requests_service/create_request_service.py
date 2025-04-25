from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common.completable import CompletableRequestsResult
from core.common.custom_errors import ErrorTypes
from core.common.decorators import close_dao_sessions
from core.dao import RequestDao
from core.models import Request


class CreateRequestService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            request: Request,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableRequestsResult:
        try:
            result = await requests_dao.create_request(request)
            return CompletableRequestsResult.ok("\/ Заявка успешно создана", request=result)
        except Exception as e:
            return CompletableRequestsResult.fail(e, message="слишком большое число", error_type=ErrorTypes.NOT_INT_32_ERROR)
