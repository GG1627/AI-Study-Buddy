import os
from upstash_redis import Redis
import time
import json

# Connect to Redis using REST API
upstash_url = os.getenv("UPSTASH_REDIS_REST_URL")
upstash_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
redis_client = Redis(url=upstash_url, token=upstash_token)

print("🚀 Testing Upstash REST connection...")
redis_client.set("test", "working")
result = redis_client.get("test")
print(f"✅ Connection successful: {result}")

# Simple worker loop that processes jobs
while True:
    try:
        # Get job from queue
        job_data = redis_client.rpop("job_queue")
        
        if job_data:
            job = json.loads(job_data)
            print(f"🔧 Processing job: {job['job_id']}")
            
            # Update job status
            job['status'] = 'processing'
            redis_client.set(f"job:{job['job_id']}", json.dumps(job))
            
            # Process the job (you'll need to implement this based on your needs)
            # For now, just mark as completed
            job['status'] = 'completed'
            job['result'] = 'Job processed successfully'
            redis_client.set(f"job:{job['job_id']}", json.dumps(job))
            
            print(f"✅ Job {job['job_id']} completed")
        else:
            print("⏳ No jobs, waiting...")
            time.sleep(5)
            
    except Exception as e:
        print(f"❌ Error processing job: {e}")
        time.sleep(10)
