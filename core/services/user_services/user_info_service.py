from dependency_injector.wiring import inject

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.dao import UserDao
from core.models import User


class UserInfoService:

    @inject
    async def execute(
            self,
            telegram_id: int
    ) -> CompletableResult:
        async with DaoContainer.session() as session:
            user_dao = UserDao(session)
            user = await user_dao.get_by_id(telegram_id)
            if user is not None:
                text = (f"id: {user.telegram_id}\n"
                        f"name: {user.name}")
                return CompletableResult.ok(text)
            else:
                text = f"Пользователь не найден"
                return CompletableResult.ok(text)

