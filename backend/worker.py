import os
import redis
from rq import Worker, Queue
import ssl

listen = ["default"]

# connect to redis using REDIS_URL from environment variable
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise ValueError("REDIS_URL environment variable is not set")
redis_conn = redis.from_url(redis_url)

if __name__ == "__main__":
    # Create queues
    queues = [Queue(name, connection=redis_conn) for name in listen]
    
    # Create and start worker
    worker = Worker(queues, connection=redis_conn)
    worker.work()