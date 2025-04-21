from telegram.ext import ApplicationBuilder

from core.presentation.commands.command_setup import setup_bot_commands, register_commands
from app.config import BOT_TOKEN
from app.service_container import ServiceContainer
from app.dao_container import DaoContainer


async def post_init(app):
    await setup_bot_commands(app.bot)

def start_application():
    service_container = ServiceContainer()
    dao_container = DaoContainer()

    service_container.wire(modules=[
        "core.presentation.handlers.utils",
        "core.presentation.handlers.users",
    ])

    dao_container.wire(modules=[
        "core.services.user_services",
    ])

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    register_commands(app)

    print("Бот запущен")

    app.run_polling()