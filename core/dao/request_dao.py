from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession

from core.common.custom_errors import ItsSoBigForIntegerError
from core.models import Request


class RequestDao:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_request(self, request: Request):
        self.session.add(request)
        try:
            await self.session.commit()
            return request
        except asyncpg.exceptions.DataError as e:
            if "value out of int32 range" in str(e):
                print("Слишком большое число! Не влезает в базу.")
                raise ItsSoBigForIntegerError("Слишком большое число! Не влезает в базу.")
            raise

    async def get_all_open_requests(self, telegram_id):
        result = await self.session.execute(
            select(Request).where(
                (Request.is_open == True) &
                (Request.creator_id != telegram_id)
            )
        )
        return result.scalars().all()

    async def get_request_by_creator_id(self, creator_id: int):
        result = await self.session.execute(
            select(Request).where(Request.creator_id == creator_id)
        )
        return result.scalars().all()

    async def get_request_by_executor_id(self, executor_id: int):
        result = await self.session.execute(
            select(Request).where(Request.executor_id == executor_id)
        )
        return result.scalars().all()

    async def get_request_file_id(self, id: int):
        result = await self.session.execute(
            select(Request).where(Request.id == id)
        )
        return result.scalar_one_or_none()

    async def add_executor_for_requests(self, id: int, executor_id: int):
        result = await self.session.execute(
            select(Request).where(
                (Request.id == id) &
                (Request.creator_id != executor_id) &
                (Request.executor_id.is_(None))  # или (Request.executor_id == None)
            )
        )
        request = result.scalar_one_or_none()

        if request:
            request.executor_id = executor_id
            await self.session.commit()
            return request
        return None

    async def add_file_id_for_requests(self, id: int, telegram_id: int, file_id: str):
        result = await self.session.execute(
            select(Request).where(
                (Request.id == id) &
                (Request.creator_id == telegram_id)
            )
        )
        request = result.scalar_one_or_none()

        if request:
            request.file_id = file_id
            await self.session.commit()
            return request
        return None

    async def close_requests(self, id: int, creator_id: int):
        result = await self.session.execute(
            select(Request).where(
                (Request.id == id) &
                (Request.creator_id == creator_id))
        )
        request = result.scalar_one_or_none()

        if request:
            request.is_open = False
            await self.session.commit()
            return request
        return None

    async def open_requests(self, id: int, creator_id: int):
        result = await self.session.execute(
            select(Request).where(
                (Request.id == id) &
                (Request.creator_id == creator_id))
        )
        request = result.scalar_one_or_none()

        if request:
            request.is_open = True
            await self.session.commit()
            return request
        return None

    async def delete_requests(self, id: int, creator_id: int):
        result = await self.session.execute(
            select(Request).where(
                (Request.id == id) &
                (Request.creator_id == creator_id))
        )
        request = result.scalar_one_or_none()

        if request:
            await self.session.delete(request)
            await self.session.commit()
            return True
        return False

    async def count_executor_requests(self, telegram_id: int):
        query = select(func.count()).where(Request.executor_id == telegram_id)
        result = await self.session.execute(query)
        return result.scalar()
