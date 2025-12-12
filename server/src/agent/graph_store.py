import time
from typing import List, Dict, Any
from .graph_config import driver
class Neo4jKnowledgeGraph:
    """Optimized Neo4j storage"""
    
    def __init__(self):
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
                            "REQUIRE (e.name, e.document_id) IS UNIQUE"
                    )
                )
        
                print("✓ Database ready\n")
            except Exception as e:
                print(f"Note: {e}\n")
    
    async def clear_database(self,document_id):
        """Clear relationships for this user/document"""
        query = """
            MATCH ()-[r:RELATED]->()
            WHERE r.document_id=$document_id
            DELETE r
        """

        async with self.driver.session() as session:
            await session.execute_write(
                lambda tx: tx.run(query,
                    document_id=document_id
                )
            )

        print(f"Database cleared for document_id={document_id}")

    
    async def store_triples_batch(self,document_id:str, triples: List[Dict[str,Any]], source: str):
        """Store triples efficiently"""
        if not triples:
            return
        
        print(f"Storing {len(triples)} triples...")
        
        # Prepare batch with new triple fields
        batch = [
            {
                "subject": triple["subject"],
                "subject_type": triple.get("subject_type", "Concept"),
                "relation": triple["relation"].upper().replace(' ', '_').replace('-', '_'),
                "object": triple["object"],
                "object_type": triple.get("object_type", "Concept"),
                "evidence": triple.get("evidence", ""),
                "formality_level": triple.get("formality_level", "conceptual"),
                "page": triple.get("page", None),
                "confidence": triple.get("confidence", "medium"),
                "source": source,
                "document_id": document_id
            }
            for triple in triples
        ]

        # Single query for all
        query = """
        UNWIND $batch as row
        MERGE (s:Entity {name: row.subject, document_id: row.document_id})
        SET s.type = row.subject_type

        MERGE (o:Entity {name: row.object, document_id: row.document_id})
        SET o.type = row.object_type

        MERGE (s)-[r:RELATED {type: row.relation, source: row.source, document_id: row.document_id}]->(o)
        ON CREATE SET 
            r.source = row.source,
            r.evidence = row.evidence, 
            r.page = row.page,
            r.confidence = row.confidence,
            r.formality_level = row.formality_level
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
        
    async def get_statistics(self,document_id:str) -> Dict:
        """Get statistics"""
        stats = {}
        async with self.driver.session() as session:     
            query1="""
                    MATCH (n:Entity)-[r:RELATED]->(m:Entity)
                    WHERE r.document_id=$document_id
                    RETURN count(DISTINCT n) AS entities,
                    count(r) AS relationships
                            """   
            result = await session.execute_write(
                lambda tx:tx.run(
                    query=query1,document_id=document_id
                )
            )
            rec=await result.single()
            stats['entities'] = rec['entities'] if rec else 0
            stats['relationships'] = rec['relationships'] if rec else 0
            
            # Get sample relationships
            query = """
            MATCH (a:Entity)-[r:RELATED]->(b:Entity)
            WHERE r.document_id=$document_id
            RETURN a.name as subject, r.type as relation, b.name as object
            LIMIT 30
            """
            
            result=await session.execute_read(
                lambda tx:tx.run(query,document_id=document_id)
            )
            sample=await result.data()
            stats['samples']=sample
        
        return stats
    
    async def show_sample(self,document_id:str,limit: int = 20):
        """Show sample relationships"""
        query = """
        MATCH (a:Entity)-[r:RELATED]->(b:Entity)
        WHERE r.document_id=$document_id
        RETURN a.name as subject, r.type as relation, b.name as object
        LIMIT $limit
        """
        async with self.driver.session() as session:
            results = await session.execute_read(
                lambda tx:tx.run(query,document_id=document_id)
            )
            samples=await results.data()
        
            print(f"\n{'='*90}")
            print(f"KNOWLEDGE GRAPH SAMPLE ({len(samples)} relationships)")
            print(f"{'='*90}\n")
            
            for r in samples:
                print(f"{r['subject']:35} --[{r['relation']}]--> {r['object']}")
            
            print(f"\n{'='*90}\n")

kg_store = Neo4jKnowledgeGraph()
