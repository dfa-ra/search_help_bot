from dependency_injector import containers, providers

from core.services import *


class ServiceContainer(containers.DeclarativeContainer):
    """Класс-контейнер отвечающий за создание сервисов"""

    # utils

    # сервис который возвращает красивый текст для вывода команды help
    help_service = providers.Factory(
        HelpService,
    )
    # сервис проверяющий лежит ли число в диапазоне int32
    is_integer_service = providers.Factory(
        IsIntegerService
    )

    # user

    # сервис регистрации нового пользователя
    register_service = providers.Factory(
        RegisterService,
    )
    # сервис который выдаёт нам информацию о  пользователе
    user_info_service = providers.Factory(
        UserInfoService,
    )
    # сервис добавления информации о пользователе
    add_info_user = providers.Factory(
        AddInfoService,
    )

    # request
    # сервис создания заявок
    create_request_service = providers.Factory(
        CreateRequestService,
    )
    # сервис красивого вывода заявок
    draw_request_service = providers.Factory(
        DrawRequestService,
    )
    # сервис который вовращает список открытых заявок
    show_all_open_requests_service = providers.Factory(
        ShowAllOpenRequestsService,
    )
    # сервис выбора заявки для выполнения
    select_request_service = providers.Factory(
        SelectRequestService,
    )
    # сервис удаления заявки по её id
    delete_request_service = providers.Factory(
        DeleteRequestService,
    )
    # сервис который возвращает список выбранных для исполнения заявок
    show_my_selected_requests_service = providers.Factory(
        ShowMySelectedRequestsService,
    )
    # сервис который возвраает все заявки созданные конкретным полььзователем
    show_my_requests_service = providers.Factory(
        ShowMyRequestsService,
    )
    # сервис который позволяет закрыть заявку по её id
    close_my_request_service = providers.Factory(
        CloseRequestService
    )
    # сервис который позволяет открыть заявку по её id
    open_my_request_service = providers.Factory(
        OpenRequestService,
    )
    # сервис который сохраняет файл заявки в mongo db
    save_request_file_service = providers.Factory(
        SaveRequestFileService
    )
    # сервис который получает файл заявки по её id
    get_request_file_service = providers.Factory(
        GetRequestFileByIdService
    )



