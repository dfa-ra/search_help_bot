from dependency_injector import containers, providers

from db.mongo.mongo import files_collection
from db.postgress.config import async_session_factory

from core.dao import *

class DaoContainer(containers.DeclarativeContainer):
    """Класс-контейнер отвечающий за создание dao"""
    # postgres
    wiring_config = containers.WiringConfiguration(packages=["core.presentation.handlers"])
    session = providers.Factory(async_session_factory)

    # mongo
    collection = providers.Factory(lambda: files_collection)

    # dao
    user_dao = providers.Factory(UserDao, session=session)
    requests_dao = providers.Factory(RequestDao, session=session)
    mongo_dao = providers.Factory(MongoDao, collection=collection)
