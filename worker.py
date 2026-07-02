import time
import json
import os
from models import init_db, SessionLocal, Event

# Wait briefly for Postgres database container to boot up completely
time.sleep(5)
init_db()

import redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

print("🚀 Background Worker started monitoring 'event_queue'...")

while True:
    try:
        # BLPOP is a blocking pull: it waits until an item enters the queue
        # '0' means wait indefinitely without timing out
        queue_name, item = redis_client.blpop("event_queue", timeout=0)
        
        if item:
            data = json.loads(item)
            print(f"📦 Worker processing event: {data}")
            
            # Save to PostgreSQL
            db = SessionLocal()
            new_event = Event(user_id=data["user_id"], action=data["action"])
            db.add(new_event)
            db.commit()
            db.refresh(new_event)
            db.close()
            
    except Exception as e:
        print(f"❌ Error processing queue item: {e}")
        time.sleep(2) # Prevent rapid loop crashing if DB drops