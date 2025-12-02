import os
from dotenv import load_dotenv
import redis
load_dotenv()
r = redis.Redis.from_url(os.getenv("REDIS_URL",""))

if r.ping():
    print("Redis is reachable")
else:
    print("Failed to connect the db")
