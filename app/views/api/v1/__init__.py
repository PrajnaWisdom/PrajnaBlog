from fastapi import APIRouter

from app.views.api.v1 import article


def register_api_v1_api_router():
    router = APIRouter()

    router.include_router(article.router, prefix="/article")
    return router


router = register_api_v1_api_router()
