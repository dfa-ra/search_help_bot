from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common.completable import CompletableResult
from core.common.decorators import close_dao_sessions
from core.dao import UserDao
from core.models import UserModel


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
            user_info: UserModel = UserModel(
                telegram_id=telegram_id,
                university=university,
                course=course,
                direction=direction,
            )
            await user_dao.add_user_info(user_info)
            return CompletableResult.ok(message=" # Спасибо за информацию о себе!")
        except Exception as e:
            return CompletableResult.fail(e, "!! Возникли неполадки с добавлением информации")
