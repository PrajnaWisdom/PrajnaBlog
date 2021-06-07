from fastapi import APIRouter

from app.service.admin.v1.captcha import captcha


router = APIRouter()


@router.get("")
async def admin_captcha():
    return captcha()
