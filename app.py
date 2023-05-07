import os
from redis import Redis
from Ayra.startup._database import RedisDB

redis_url = os.environ.get("REDISCLOUD_URL", "")
if redis_url.startswith("redis://"):
    redis_url = redis_url.replace("redis://", "", 1)
    redis_uri, redis_password = redis_url.split("@")
    redis_password = redis_password.split(":")[0]
    host_port = redis_uri.split(":")
    host = host_port[0]
    port = int(host_port[1])
    redis_db = RedisDB(
        host=host,
        port=port,
        password=redis_password
    )
else:
    raise ValueError("Invalid REDISCLOUD_URL")

