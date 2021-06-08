import uuid
import base64
import random
from PIL import ImageFilter
from captcha.image import ImageCaptcha, random_color

from app.corelibs.redis import cache
from app.exc.consts import CACHE_ADMIN_CAPTCHA_VALUE, CACHE_FIVE_MINUTE


def random_text(length=4):
    return ''.join(random.sample('0123456789', length))


class Captcha(ImageCaptcha):
    def generate_image(self, chars):
        """Generate the image of the given characters.

        :param chars: text to be generated.
        """
        background = random_color(238, 255)
        color = random_color(10, 200, random.randint(220, 255))
        im = self.create_captcha_image(chars, color, background)
        im = im.filter(ImageFilter.SMOOTH)
        return im

    def generate_image_captcha(self, length=4):
        chars = random_text(length)
        uid = uuid.uuid4().hex
        image_data = self.generate(chars)
        image_data_b64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
        cache.set(CACHE_ADMIN_CAPTCHA_VALUE.format(uuid), chars, CACHE_FIVE_MINUTE)
        return uid, chars, image_data_b64

    @classmethod
    def check_captcha(cls, captcha_id, captcha):
        result = cache.get(CACHE_ADMIN_CAPTCHA_VALUE.format(captcha_id))
        if not result:
            return False
        if result != captcha:
            return False
        return True
