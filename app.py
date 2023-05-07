import os

redis_url = os.environ.get("REDISCLOUD_URL", "")
if redis_url.startswith("redis://"):
    redis_url = redis_url.replace("redis://", "", 1)
    redis_uri, redis_password = redis_url.split("@")
    redis_password = redis_password.split(":")[0]
    host_port = redis_uri.split(":")
    host = host_port[0]
    port = int(host_port[1])

    # Set REDIS_URI and REDIS_PASSWORD as environment variables
    os.environ["REDIS_URI"] = f"redis://{host}:{port}"
    os.environ["REDIS_PASSWORD"] = redis_password

else:
    raise ValueError("Invalid REDISCLOUD_URL")
