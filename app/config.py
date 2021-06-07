from app.utils.logger import logger


SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3307/prajna_blog?charset=utf8mb4"

REDIS_URL = "redis://127.0.0.1:6379/0"
REDIS_MAX_CONNECTIONS = 100


try:
    from local_settings import *  # noqa
except Exception:
    logger.error("local_settings import ERROR")
