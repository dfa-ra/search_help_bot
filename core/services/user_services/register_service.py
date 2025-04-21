from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from app.dao_container import DaoContainer
from core.common import CompletableResult
from core.dao import UserDao
from core.models import User


class RegisterService:

    @inject
    async def execute(
            self,
            user: User,
    ) -> CompletableResult:
        async with DaoContainer.session() as session:
            user_dao = UserDao(session)
            try:
                await user_dao.create_user(user)
                return CompletableResult.ok()
            except IntegrityError as e:
                return CompletableResult.fail(e)
