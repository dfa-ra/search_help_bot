from dependency_injector.wiring import inject
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.dao import RequestDao
from core.models import Request


class CreateRequestService:

    @inject
    async def execute(
            self,
            request: Request,
    ) -> CompletableResult:
        async with DaoContainer.session() as session:
            request_dao = RequestDao(session)
            try:
                await request_dao.create_request(request)
                return CompletableResult.ok("\/ Заявка успешно создана")
            except IntegrityError as e:
                return CompletableResult.fail(e, "!! Не удалось зарегестироавть заявку")
