import os
from urllib.parse import urlparse

from Ayra.startup._database import RedisDB

redis_url = os.environ.get("REDISCLOUD_URL")
if redis_url:
    url = urlparse(redis_url)
    redis_db = RedisDB(
        host=url.hostname,
        port=url.port,
        password=url.password,
    )
    REDIS_URI = f"redis://{url.hostname}:{url.port}"
    REDIS_PASSWORD = url.password
else:
    raise ValueError("Invalid REDISCLOUD_URL")
