from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common.completable import CompletableResult
from core.common.decorators import close_dao_sessions
from core.dao import UserDao
from core.models import User


class AddInfoService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            telegram_id: int,
            university: str,
            course: int,
            direction: str,
            user_dao: UserDao = Provide[DaoContainer.user_dao],
    ) -> CompletableResult:
        try:
            await user_dao.add_user_info(telegram_id, university, course, direction)
            return CompletableResult.ok(message=" # Спасибо за информацию о себе!")
        except Exception as e:
            return CompletableResult.fail(e, "!! Возникли неполадки с добавлением информации")
