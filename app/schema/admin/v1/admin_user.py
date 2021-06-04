from pydantic import BaseModel


class Login(BaseModel):
    account: str
    password: str
    captcha: str
    captchaID: str
