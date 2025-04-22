from dependency_injector import containers, providers

from core.services import *


class ServiceContainer(containers.DeclarativeContainer):
    # utils
    help_service = providers.Factory(
        HelpService,
    )

    # user
    register_service = providers.Factory(
        RegisterService,
    )
    user_info_service = providers.Factory(
        UserInfoService,
    )

    # request
    create_request_service = providers.Factory(
        CreateRequestService,
    )
    draw_request_service = providers.Factory(
        DrawRequestService,
    )
    show_all_open_requests_service = providers.Factory(
        ShowAllOpenRequestsService,
    )
    select_request_service = providers.Factory(
        SelectRequestService,
    )
    delete_request_service = providers.Factory(
        DeleteRequestService,
    )
    show_my_selected_requests_service = providers.Factory(
        ShowMySelectedRequestsService,
    )
    show_my_requests_service = providers.Factory(
        ShowMyRequestsService,
    )
    close_my_request_service = providers.Factory(
        CloseRequestService
    )
    open_my_request_service = providers.Factory(
        OpenRequestService,
    )


