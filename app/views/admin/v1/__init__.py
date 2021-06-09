from fastapi import APIRouter, Request, Response, status

from app.views.admin.v1 import admin_user, captcha, articles
from app.corelibs.redis import cache
from app.exc.consts import CACHE_ADMIN_USER_TOKEN


def register_admin_v1_api_router():
    router = APIRouter()

    router.include_router(admin_user.router, prefix="/admin")
    router.include_router(captcha.router, prefix="/captcha")
    router.include_router(articles.router, prefix="/article")
    return router


def admin_user_token(app):
    NOT_NEED_TOKEN_PATH = ("/docs", "/openapi.json", "/admin/v1/captcha", "/admin/v1/admin/login")

    @app.middleware("http")
    async def need_check_admin_user_token(request: Request, call_next):
        path = request.scope["path"]
        if path not in NOT_NEED_TOKEN_PATH:
            token = request.headers.get("token")
            if not token:
                return Response(status_code=status.HTTP_403_FORBIDDEN)
            admin_id = cache.get(CACHE_ADMIN_USER_TOKEN.format(token))
            if not AdminUser.get(admin_id):
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        return await call_next(request)


router = register_admin_v1_api_router()


from app.models.admin_user import AdminUser
