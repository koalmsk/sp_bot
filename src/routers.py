from handlers.admin_handlers import admin_handler_route
from handlers.user_handlers import user_handler_route
from callback.admin_callback import admin_callback_router
from callback.user_callback import user_callback_router

routers = [
    user_handler_route,
    user_callback_router,
    admin_callback_router,
    admin_handler_route,
]
