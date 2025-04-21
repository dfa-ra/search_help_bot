from dependency_injector import containers, providers

from core.services.help_service import HelpService
from core.services.user_services import RegisterService

class ServiceContainer(containers.DeclarativeContainer):
    help_service = providers.Factory(
        HelpService,
    )
    register_service = providers.Factory(
        RegisterService,
    )