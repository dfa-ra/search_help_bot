from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Integer

from core.models import UserModel


class UserDao:
    """класс отвечающий за взаимодействие с табличкой user-ов"""
    def __init__(self, session: AsyncSession):
        self.session = session

    # создать юзера
    async def create_user(self, user: UserModel):
        self.session.add(user)
        await self.session.commit()
        return user

    # получить юзера по его telegram_id
    async def get_by_id(self, telegram_id: int) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    # добавить информацию о юзере
    async def add_user_info(
            self,
            user_info: UserModel
    ) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == user_info.telegram_id)
        )
        user: UserModel = result.scalar_one_or_none()

        if user:
            user.university = user_info.university
            user.course = user_info.course
            user.direction = user_info.direction
            await self.session.commit()
            return user
        return None