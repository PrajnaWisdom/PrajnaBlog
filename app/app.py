from fastapi import FastAPI

from app.views.admin.v1 import admin_user_token, router as admin_v1_router
from app.views.api.v1 import router as api_v1_router


def create_app():
    app = FastAPI()

    app.include_router(admin_v1_router, prefix="/admin/v1")
    app.include_router(api_v1_router, prefix="/api/v1")

    admin_user_token(app)
    return app
