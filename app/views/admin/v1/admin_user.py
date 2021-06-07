from fastapi import APIRouter, Header
from app.service.admin.v1.admin_user import login, logout
from app.schema.admin.v1.admin_user import Login


router = APIRouter()


@router.post("/login")
async def admin_login(loginForm: Login):
    return login(loginForm)


@router.post("/logout")
async def admin_logout(token: str = Header(None)):
    return logout(token)
