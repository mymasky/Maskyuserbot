import os
from dotenv import load_dotenv, set_key

load_dotenv()

redis_url = os.environ.get("REDISCLOUD_URL", "")

if redis_url.startswith("redis://"):
    redis_url = redis_url.replace("redis://", "", 1)
    redis_uri, redis_password = redis_url.split("@")
    redis_password = redis_password.split(":")[1]
    
    os.environ["REDIS_URI"] = redis_uri
    set_key(".env", "REDIS_URI", redis_uri)
    os.environ["REDIS_PASSWORD"] = redis_password
    set_key(".env", "REDIS_PASSWORD", redis_password)

else:
    raise ValueError("Invalid REDISCLOUD_URL")
