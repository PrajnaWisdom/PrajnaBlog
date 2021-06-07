from fastapi import FastAPI

from app.views.admin.v1 import router as admin_v1_router


def create_app():
    app = FastAPI()

    app.include_router(admin_v1_router, prefix="/admin/v1")

    return app
