from core.models import RequestModel


class DrawRequestService:
    async def execute(
            self,
            request: RequestModel,
    ) -> str:
        str = (f"# Заявка №{request.id}\n\n\n"
               f"Тема: {request.topic}\n\n"
               f"Основное описание: {request.main_text}\n\n"
               f"Дедлайн: {request.deadline}\n\n"
               f"Цена: {request.money}\n\n")

        if (request.executor_id != None):
            str += f"В работе\n\n"
        else:
            str += f"Свободна\n\n"
        return str