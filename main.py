from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import redis
import json
import os

app = FastAPI(title="Analytics Ingestion Engine")

# Connect to Redis container using its Docker service name 'redis'
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

class EventSchema(BaseModel):
    user_id: str
    action: str

@app.post("/events", status_code=202)
def ingest_event(event: EventSchema):
    try:
        # Convert Pydantic object to JSON string
        event_data = json.dumps(event.model_dump())
        
        # Push to the back of the Redis list (Queue)
        redis_client.rpush("event_queue", event_data)
        
        return {"status": "Accepted", "message": "Event queued successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}