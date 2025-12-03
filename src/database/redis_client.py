import os
from dotenv import load_dotenv
import redis
load_dotenv()
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL",""))
