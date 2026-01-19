import asyncio
import json
from src.agent.builder import build_knowledge_graph
from src.celery_app import celery
from src.database.redis_client import redis_client

@celery.task
def build_kg_task(pdf_path, document_id, provider="gemini", model="gemini-2.5-flash", quality="L"):
    # background tasks
    asyncio.run(
    build_knowledge_graph(
        pdf_path=pdf_path,
        document_id=document_id,
        provider=provider,
        model=model,
        quality=quality
    )
    )
    payload=json.dumps({
        "document_id":document_id,
        "status":True
    })
    #once task is complete, status broadcasted via redis. Any process registered to this channel will be notified about the status
    redis_client.set(f"status:{document_id}", "completed", ex=3600)
    redis_client.publish(f"channel:{document_id}", payload)
