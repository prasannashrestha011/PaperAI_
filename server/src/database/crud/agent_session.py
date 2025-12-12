import json
from src.database.redis_client import redis_client
from src.agent.agent import Neo4jRAGSystem

async def get_agent_session(user_id:str,document_id:str,provider,model):
    key=f"agent:{user_id}-{document_id}"
    data =await redis_client.get(key)
    if data:
        config=json.loads(data)
    else:
        config={
            "user_id":user_id,
            "document_id":document_id,
            "provider":provider,
            "model":model
        }
        await redis_client.setex(key,1800,json.dumps(config,default=str))

    await redis_client.expire(key,1800)
    agent=Neo4jRAGSystem(
        user_id=config["user_id"],
        document_id=config["document_id"],
        provider=config["provider"],
        model=config["model"]
    )
        

    return agent


