import os
import redis
from rq import Worker, Queue

listen = ["default"]

# Get Redis URL
redis_url = os.getenv("REDIS_URL")
print(f"REDIS_URL found: {redis_url is not None}")

if not redis_url:
    raise ValueError("REDIS_URL environment variable is not set")

# Test connection exactly like Upstash docs
try:
    print("🔄 Testing Upstash connection...")
    r = redis.Redis.from_url(redis_url)
    
    # Test basic operations (like Upstash example)
    print("🔄 Testing SET/GET...")
    r.set('test_foo', 'test_bar')
    value = r.get('test_foo')
    print(f"✅ SET/GET test successful: {value}")
    
    # Use this connection for RQ
    redis_conn = r
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print(f"❌ Error type: {type(e)}")
    raise

if __name__ == "__main__":
    try:
        print("🔄 Creating RQ queues...")
        queues = [Queue(name, connection=redis_conn) for name in listen]
        
        print("🔄 Creating RQ worker...")
        worker = Worker(queues, connection=redis_conn)
        
        print("✅ Starting worker...")
        worker.work()
        
    except Exception as e:
        print(f"❌ RQ Worker failed: {e}")
        raise