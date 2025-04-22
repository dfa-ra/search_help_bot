from dependency_injector.wiring import inject
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.dao import RequestDao

class SelectRequestService:

    @inject
    async def execute(
            self,
            id: int,
            telegram_id: int
    ) -> CompletableResult:
        async with DaoContainer.session() as session:
            request_dao = RequestDao(session)
            count = await request_dao.count_executor_requests(telegram_id)
            if count > 2:
                return CompletableResult.ok(f"!! Вы и так выполняете уже более 2 заявок")
            try:
                result = await request_dao.add_executor_for_requests(id, telegram_id)
                if result is not None:
                    return CompletableResult.ok(f"\/ Заявка №{id} закреплена за вами")
                else:
                    return CompletableResult.ok(f"!! Данная заявка №{id} не может быть закреплена за вами так как она либо в работе либо является вашей заявкой")
            except Exception as e:
                return CompletableResult.fail(e, f"!! Не закрепить за вами заявку №{id}")
