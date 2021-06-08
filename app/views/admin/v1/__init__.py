from fastapi import APIRouter

from app.views.admin.v1 import admin_user, captcha, articles


def register_admin_v1_api_router():
    router = APIRouter()

    router.include_router(admin_user.router, prefix="/admin")
    router.include_router(captcha.router, prefix="/captcha")
    router.include_router(articles.router, prefix="/article")
    return router


router = register_admin_v1_api_router()
