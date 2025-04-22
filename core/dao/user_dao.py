from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Integer

from core.models import User


class UserDao:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_by_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def add_user_info(
            self,
            telegram_id: int,
            university: str,
            course: int,
            direction: str
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user: User = result.scalar_one_or_none()

        if user:
            user.university = university
            user.course = course
            user.direction = direction
            await self.session.commit()
            return user
        return None