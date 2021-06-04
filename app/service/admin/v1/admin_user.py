import shortuuid

from app.models.admin_user import AdminUser
from app.schema.admin.v1.admin_user import Login
from app.corelibs.redis import cache
from app.external.captcha import Captcha
from app.exc.codes import BIZ_CODE_ADMIN_USER_NOT_EXISTS, BIZ_CODE_CAPTCHA_ERROR
from app.exc.consts import CACHE_ADMIN_USER_TOKEN, CACHE_TWELVE_HOUR
from app.utils.api import Response


async def login(login: Login):
    admin_user = AdminUser.get_by_account(login.account)
    if not Captcha.check_captcha(login.captchaID, login.captcha):
        return Response.response(code=BIZ_CODE_CAPTCHA_ERROR)
    if not admin_user:
        return Response.response(code=BIZ_CODE_ADMIN_USER_NOT_EXISTS)
    if not admin_user.check_password_hash(login.password):
        return Response.response(code=BIZ_CODE_ADMIN_USER_NOT_EXISTS, message="账号或密码错误")
    token = shortuuid.uuid()
    cache.set(CACHE_ADMIN_USER_TOKEN.format(token), admin_user.id, CACHE_TWELVE_HOUR)
    result = {
        "token": token,
        "expired_at": CACHE_TWELVE_HOUR,
        "id": admin_user.id,
    }
    return Response.success(data=result)


async def logout(token: str):
    cache.delete(CACHE_ADMIN_USER_TOKEN.format(token))
    return Response.success()
