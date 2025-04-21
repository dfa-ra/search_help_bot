from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


class UserDao:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        return user
