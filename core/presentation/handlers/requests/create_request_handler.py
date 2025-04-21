from dependency_injector.wiring import inject
from telegram import Update
from telegram.ext import ContextTypes


@inject
async def create_requests_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
):
    pass
