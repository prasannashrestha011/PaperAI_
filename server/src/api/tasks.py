"""
Implementation of web hooks to notify client side about completion of knowledge graph.
To handle background task, celery has been registered on doc upload api.
Once task has been queued and completed, the websocket connection here will broad cast the message to the client.
Workflow:
    Client->Doc upload-> celery_queue[KG building]-> status-> web socket -> client
Note: 
    Client will be registered to this socket connection during doc upload
"""

from fastapi import APIRouter,WebSocket

from src.database.redis_client import redis_client


router=APIRouter(prefix="/task")

@router.websocket("/kg-status/{id:path}")
async def check_task_status(websocket:WebSocket,id:str):
    await websocket.accept()
    pubsub=redis_client.pubsub()
    await pubsub.subscribe(f"channel:{id}")
