import time
from typing import List, Dict, Any
from .graph_config import driver
class Neo4jKnowledgeGraph:
    """Optimized Neo4j storage"""
    
    def __init__(self,session_id:str):
        self.session_id=session_id
        self.driver=driver
    
    async def initialize(self):
        """Initialize database"""
        print("Initializing Neo4j...")
        async with self.driver.session() as session:
            try:
 
                await session.execute_write(
                    lambda tx:tx.run(
                              "CREATE CONSTRAINT entity_name IF NOT EXISTS "
                             "FOR (e:Entity) "
                            "REQUIRE (e.name, e.session_id) IS UNIQUE"
                    )
                )
        
                print("✓ Database ready\n")
            except Exception as e:
                print(f"Note: {e}\n")
    
    async def clear_database(self):
        """Clear relationships for this user/document"""
        query = """
            MATCH ()-[r:RELATED]->()
            WHERE r.session_id=$session_id
            DELETE r
        """

        async with self.driver.session() as session:
            await session.execute_write(
                lambda tx: tx.run(query,
                    session_id=self.session_id
                )
            )

        print(f"Database cleared for session_id={self.session_id}")

    
    async def store_triples_batch(self, triples: List[Dict[str,Any]], source: str):
        """Store triples efficiently"""
        if not triples:
            return
        
        print(f"Storing {len(triples)} triples...")
        
        # Prepare batch
        batch = [
        {
            "subject": triple["subject"],
            "relation": triple["relation"].upper().replace(' ', '_').replace('-', '_'),
            "object": triple["object"],
            "evidence": triple.get("evidence", ""),
            "page": triple.get("page", None),
            "confidence": triple.get("confidence", "medium"),
            "source": source,
            "session_id":self.session_id
        }
        for triple in triples
        ]
        
        # Single query for all
        query = """
        UNWIND $batch as row
        MERGE (s:Entity {name: row.subject,session_id:row.session_id})
        MERGE (o:Entity {name: row.object,session_id:row.session_id})
        MERGE (s)-[r:RELATED {type: row.relation,source:row.source,session_id:row.session_id}]->(o)
       ON CREATE SET 
                r.source = row.source,
                r.evidence=row.evidence, 
                r.page=row.page,
                r.confidence=row.confidence
         """
        
        async with self.driver.session() as session:
            try:
                start=time.perf_counter()
                await session.execute_write(
                    lambda tx:tx.run(query,batch=batch)
                )
                end=time.perf_counter()
                print(f"Storing time taken: {end-start:.4f}")
                print(f"Stored successfully\n")
            except Exception as e:
                print(f"Storage error: {e}\n")
                raise
        
    async def get_statistics(self) -> Dict:
        """Get statistics"""
        stats = {}
        async with self.driver.session() as session:     
            query1="""
                    MATCH (n:Entity)-[r:RELATED]->(m:Entity)
                    WHERE r.session_id=$session_id
                    RETURN count(DISTINCT n) AS entities,
                    count(r) AS relationships
                            """   
            result = await session.execute_write(
                lambda tx:tx.run(
                    query=query1,session_id=self.session_id
                )
            )
            rec=await result.single()
            stats['entities'] = rec['entities'] if rec else 0
            stats['relationships'] = rec['relationships'] if rec else 0
            
            # Get sample relationships
            query = """
            MATCH (a:Entity)-[r:RELATED]->(b:Entity)
            WHERE r.session_id=$session_id
            RETURN a.name as subject, r.type as relation, b.name as object
            LIMIT 30
            """
            
            result=await session.execute_read(
                lambda tx:tx.run(query,session_id=self.session_id)
            )
            sample=await result.data()
            stats['samples']=sample
        
        return stats
    
    async def show_sample(self, limit: int = 20):
        """Show sample relationships"""
        query = """
        MATCH (a:Entity)-[r:RELATED]->(b:Entity)
        WHERE r.session_id=$session_id
        RETURN a.name as subject, r.type as relation, b.name as object
        LIMIT $limit
        """
        async with self.driver.session() as session:
            results = await session.execute_read(
                lambda tx:tx.run(query,session_id=self.session_id)
            )
            samples=await results.data()
        
            print(f"\n{'='*90}")
            print(f"KNOWLEDGE GRAPH SAMPLE ({len(samples)} relationships)")
            print(f"{'='*90}\n")
            
            for r in samples:
                print(f"{r['subject']:35} --[{r['relation']}]--> {r['object']}")
            
            print(f"\n{'='*90}\n")

