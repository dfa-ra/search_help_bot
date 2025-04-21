from dependency_injector import containers, providers

from core.dao import UserDao
from db.config import async_session_factory


class DaoContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["core.presentation.handlers"])

    session = providers.Factory(async_session_factory)
    user_dao = providers.Factory(UserDao, session=session)
