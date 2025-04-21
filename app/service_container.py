from dependency_injector import containers, providers

from core.services import *


class ServiceContainer(containers.DeclarativeContainer):
    help_service = providers.Factory(
        HelpService,
    )
    register_service = providers.Factory(
        RegisterService,
    )
    user_info_service = providers.Factory(
        UserInfoService,
    )
