from .handlers import commands, bot_replyes, register



routers = [
    commands.router,
    bot_replyes.router,
    register.router
]

__all__ = [
    'routers'
]