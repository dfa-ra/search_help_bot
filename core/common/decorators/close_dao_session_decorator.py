from sqlalchemy.ext.asyncio import AsyncSession
from functools import wraps
import inspect


def close_dao_sessions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)

        bound_args = inspect.signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()

        for arg in bound_args.arguments.values():
            if hasattr(arg, "session") and isinstance(arg.session, AsyncSession):
                try:
                    await arg.session.close()
                except Exception as e:
                    pass

        return result

    return wrapper
