from dependency_injector.wiring import inject, Provide

from app.dao_container import DaoContainer
from core.common.completable import CompletableResult
from core.common.decorators import close_dao_sessions
from core.dao import UserDao
from core.models import UserModel


class UserInfoService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            telegram_id: int,
            user_dao: UserDao = Provide[DaoContainer.user_dao],
    ) -> CompletableResult:
        user = await user_dao.get_by_id(telegram_id)
        if user is not None:
            text = (f"Вот это ты если чё\n\n"
                    f"Имя: {user.name}\n"
                    f"Университет: {user.university}\n"
                    f"Курс: {user.course}\n"
                    f"Направление: {user.direction}")
            return CompletableResult.ok(text)
        else:
            text = f"Пользователь не найден"
            return CompletableResult.ok(text)

