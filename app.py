import os
from redis import Redis

redis_url = os.environ.get("REDISCLOUD_URL", "")

if redis_url.startswith("redis://"):
    redis_url = redis_url.replace("redis://", "", 1)
    redis = Redis.from_url(redis_url)
    host, port, password = redis.connection_pool.connection_kwargs.values()

    os.environ["REDIS_URI"] = f"redis://{host}:{port}"
    os.environ["REDIS_PASSWORD"] = password

else:
    raise ValueError("Invalid REDISCLOUD_URL")
