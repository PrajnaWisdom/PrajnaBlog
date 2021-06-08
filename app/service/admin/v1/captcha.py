from app.external.captcha import Captcha
from app.utils.api import Response


def captcha():
    uid, _, image_data = Captcha().generate_image_captcha()
    return Response.success(data={
        "captcha_id": uid,
        "b64s": image_data
    })
