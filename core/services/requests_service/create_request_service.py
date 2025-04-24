from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.common.CustomErrors import ItsSoBigForIntegerError, ErrorTypes
from core.dao import RequestDao
from core.models import Request


class CreateRequestService:

    @inject
    async def execute(
            self,
            request: Request,
            requests_dao: RequestDao = Provide[DaoContainer.requests_dao],
    ) -> CompletableResult:
        try:
            await requests_dao.create_request(request)
            return CompletableResult.ok("\/ Заявка успешно создана")
        except Exception as e:
            return CompletableResult.fail(e, message="слишком большое число", error_type=ErrorTypes.NOT_INT_32_ERROR)
