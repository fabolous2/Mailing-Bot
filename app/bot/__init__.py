from .handlers import commands



routers = [
    commands.router,
]

__all__ = [
    'routers'
]