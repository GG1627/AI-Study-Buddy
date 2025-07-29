import os
import redis
from rq import Worker, Queue

listen = ["default"]

# connect to redis
redis_conn = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
)

if __name__ == "__main__":
    # Create queues
    queues = [Queue(name, connection=redis_conn) for name in listen]
    
    # Create and start worker
    worker = Worker(queues, connection=redis_conn)
    worker.work()