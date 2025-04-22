from dependency_injector.wiring import inject

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.dao import RequestDao


class OpenRequestService:

    @inject
    async def execute(
            self,
            id: int,
            telegram_id: int
    ) -> CompletableResult:
        async with DaoContainer.session() as session:
            request_dao = RequestDao(session)
            try:
                result: bool = await request_dao.open_requests(id, telegram_id)
                if result:
                    return CompletableResult.ok(f"\/ Заявка №{id} успешно открыта")
                else:
                    return CompletableResult.ok(f"!! Заявку №{id} открыть не получилоось, возможно вы не являетесь создателем этой заявки")
            except Exception as e:
                return CompletableResult.fail(e, "!! Произошла ошибка при открытии заявки")
