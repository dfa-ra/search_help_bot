from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common.completable import CompletableResult
from core.common.decorators import close_dao_sessions
from core.dao import UserDao
from core.models import User


class RegisterService:

    @inject
    @close_dao_sessions
    async def execute(
            self,
            user: User,
            user_dao: UserDao = Provide[DaoContainer.user_dao],
    ) -> CompletableResult:
        try:
            await user_dao.create_user(user)
            return CompletableResult.ok()
        except IntegrityError as e:
            return CompletableResult.fail(e, "Данный пользователь уже зарегестрирован")
