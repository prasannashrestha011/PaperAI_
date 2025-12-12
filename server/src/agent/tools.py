"""
Query tools for graph operations
This tools will be used by the agent for context retrieval
"""
from langchain_core.tools import tool,BaseTool
from .graph_config import driver
from typing import List,Dict,Any      
from langchain_core.documents import Document
import json
import spacy
def _create_kg_search_tool(document_id:str) -> BaseTool:
        """Create knowledge graph search tool for agent"""
        nlp_model = spacy.load("en_core_web_sm")
        @tool
        async def search_kg(query: str, document_id: str):
            """Search the knowledge graph for relevant relationships with extended triple schema."""
            try:
                doc = nlp_model(query)

                # Extract entities from query
                entities = [ent.text.lower() for ent in doc.ents]

                if not entities:
                    entities = [
                        token.text.lower()
                        for token in doc
                        if not token.is_stop
                        and not token.is_punct
                        and len(token.text) > 2
                        and token.pos_ in ["NOUN", "PROPN"]
                    ]

                if not entities:
                    return "[]"

                results_json = []
                seen = set()

                query_cypher = """
                    MATCH (n:Entity)-[r:RELATED]->(m:Entity)
                    WHERE (toLower(n.name) CONTAINS $entity OR toLower(m.name) CONTAINS $entity)
                    AND r.document_id = $document_id
                    RETURN n.name AS subject, n.type AS subject_type,
                        r.type AS relation, r.evidence AS evidence,
                        r.page AS page, r.confidence AS confidence,
                        m.name AS object, m.type AS object_type
                    LIMIT $limit
                """

                async with driver.session() as session:
                    for entity in entities[:5]:
                        try:
                            result = await session.run(
                                query_cypher,
                                entity=entity.lower(),
                                document_id=document_id,
                                limit=50,
                            )
                            records = [record async for record in result]

                            for rec in records:
                                row = rec.data()
                                subj = row.get("subject")
                                obj = row.get("object")
                                rel = row.get("relation")
                                evidence = row.get("evidence", "")
                                page = row.get("page", "NAN")
                                confidence = row.get("confidence", "medium")
                                sub_type = row.get("subject_type", "Concept")
                                obj_type = row.get("object_type", "Concept")

                                if not subj or not obj or not rel:
                                    continue

                                # Normalize relation
                                rel_norm = "_".join(rel.strip().split()).lower()

                                key = f"{subj}→{rel_norm}→{obj}"
                                if key in seen:
                                    continue
                                seen.add(key)

                                # Escape evidence
                                evidence = evidence.replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")

                                results_json.append({
                                    "subject": subj,
                                    "subject_type": sub_type,
                                    "relation": rel_norm,
                                    "object": obj,
                                    "object_type": obj_type,
                                    "evidence": evidence,
                                    "formality_level": "conceptual",  # default
                                    "page": page,
                                    "confidence": confidence
                                })

                        except Exception as e:
                            print(f"Query error for entity={entity}: {e}")

                return json.dumps(results_json, indent=2) if results_json else "[]"

            except Exception as e:
                return f"Error searching knowledge graph: {str(e)}"


        return search_kg
 

    
def _create_kg_entity_lookup_tool(document_id:str) -> BaseTool:
        """Create tool to get all relationships for a specific entity"""
        
        @tool
        async def entity_lookup(entity_name: str) -> str:
            """
            Get ALL relationships for a specific entity from the knowledge graph.
            Input should be the exact or partial name of an entity (e.g., "ReAct", "Chain-of-Thought").
            Returns all relationships where this entity is the subject.
            Use this when you need comprehensive information about a specific concept.
            """
            try:
                query = """
                MATCH (e)-[r]->(target)
                WHERE toLower(e.name) CONTAINS toLower($entity) AND r.document_id=$document_id
                RETURN e.name + ' --' + type(r) + '--> ' + target.name AS relationship, r.evidence as evidence
                LIMIT 20
                """
                
                async with driver.session() as session:
                    results = await session.run(query, entity=entity_name,document_id=document_id)
                    records= [record async for record in results]
                
                if not records:
                    return f"No relationships found for entity: {entity_name}"  
                
                # Safely extract relationships
                relationships = []
                for r in records:
                    rec=r.data()
                    if rec and "relationship" in rec:
                        relationship = rec["relationship"]
                        evidence = rec.get("evidence", "No evidence")
                        relationships.append(f"{relationship}\n  evidence: {evidence}")
                
                return "\n".join(relationships) if relationships else "No relationships found"
            
            except Exception as e:
                return f"Error looking up entity: {str(e)}"
        
        return entity_lookup

def _create_multi_hop_tool(document_id:str) -> BaseTool:
        """Create tool for multi-hop reasoning queries"""
        
        @tool
        async def multi_hop_search(path_query: str) -> str:
            """
            Find indirect relationships and reasoning paths between concepts.
            Input should describe what you're trying to connect (e.g., "ReAct to evaluation metrics").
            Returns paths showing how concepts are connected through intermediate entities.
            Use this for complex questions requiring chaining multiple relationships.
            """
            try:
                # Simple multi-hop query
                query = """
                  MATCH path = (start)-[*1..3]->(end)
WHERE (toLower(start.name) CONTAINS $user_query
   OR toLower(end.name) CONTAINS $user_query)
AND ALL(rel IN relationships(path) WHERE rel.document_id = $document_id)
WITH path, length(path) AS pathLength
ORDER BY pathLength
LIMIT 10
RETURN
    [node IN nodes(path) | node.name] AS entities,
    [rel IN relationships(path) | type(rel)] AS relations,
    [rel IN relationships(path) | rel.evidence] AS evidence;

                """
                
                async with driver.session() as session:
                    results = await session.run(query, user_query=path_query,document_id=document_id)
                    records=[record async for record in results]
                
                if not records:
                    return "No multi-hop paths found."
                
                formatted = []
                for i, record in enumerate(records, 1):
                    rec = record.data()
                    if not rec:
                        continue

                    entities = rec.get("entities", [])
                    relations = rec.get("relations", [])
                    evidence = rec.get("evidence", [])

                    if not entities or not relations:
                        continue

                    path_parts = []
                    for j in range(len(entities) - 1):
                        if j < len(relations):
                            rel = relations[j]
                            ev = evidence[j] if j < len(evidence) else "No evidence"

                            path_parts.append(
                                f"{entities[j]} --{rel}--> {entities[j+1]} (evidence: {ev})"
                            )

                    if path_parts:
                        formatted.append(f"{i}. {' | '.join(path_parts)}")

                return "\n".join(formatted) if formatted else "No valid paths found"

            
            except Exception as e:
                return f"Error in multi-hop search: {str(e)}"
        
        return multi_hop_search
    

def _create_structured_retrieval_tools(document_id:str)->List[BaseTool]:
     
    @tool
    async def paper_lookup():
        """
        Retrieve basic paper information.
        
        Use this tool when you need to:
        - Get the paper title from a session ID
        - Verify if a paper exists in the system
        - Get basic paper metadata
        
            
        Returns:
            Dictionary containing paper title and document_id, or None if not found
        """

        query="""
            MATCH (p:Paper {document_id:$document_id})
            RETURN p
            """
        async with driver.session() as session:
            result = await session.run(query, document_id=document_id)
            records = [record async for record in result]
        if not records:
            print("404")
            return
        paper=records[0]["p"]
        if not paper:
              return
        paper_data={
              "title":paper["title"],
              "document_id":paper["document_id"]
        }
        return paper_data
    
    @tool 
    async def author_lookup()->List[Dict[str,Any]]:
        """
        Retrieve all authors who wrote a specific paper.
        
        Use this tool when you need to:
        - Find out who wrote a paper
        - Get author contact information (email)
        - Get author affiliations and institutions
        - Answer questions like "Who are the authors of this paper?" or "What is the author's email?"

            
        Returns:
            List of dictionaries, each containing author name, affiliations (list), and email
        """

        query="""
                MATCH (a:Author)-[AUTHORED]->(p:Paper {document_id:$document_id})
                RETURN a as author
             """
        async with driver.session() as session:
            results = await session.run(query, document_id=document_id)
            records = [record async for record in results]
        
        authors=[]
        for record in records:
            rec=record.data()
            if not record:
                continue
            author=rec["author"]
            if not author:
                 continue 
            name=author["name"]
            affiliations=author["affiliations"]
            email=author["email"]
            authors.append({"name":name,"affiliations":affiliations,"email":email})
        
        return authors
    @tool 
    async def section_lookup()->List[Dict[str,Any]]:
        """
        Retrieve all sections of a paper with their content and metadata.
        
        Use this tool when you need to:
        - Get the structure of a paper (Introduction, Methodology, Results, etc.)
        - Find content from a specific section (e.g., "What does the Introduction say?")
        - Get page numbers where sections start
        - Answer questions about paper organization or specific section content

            
        Returns:
            List of dictionaries, each containing section_name, start_page, content, and confidence level
        """
        
        query="""
            MATCH (p:Paper {document_id:$document_id})-[r:HAS_SECTION]->(s:Section)
            RETURN s as section        
            """   
        
        async with driver.session() as session:
            results = await session.run(query, document_id=document_id)
            records = [record async for record in results]
        sections=[]
        for record in records:
            if not record:
                continue
            rec=record.data()
            section_node=rec["section"]
            if not section_node:
                continue 
            
            section={
                "document_id":document_id,
                "section_name":section_node["section_name"],
                "start_page":section_node["start_page"],
                "evidence":section_node["content"],
                "confidence":section_node["confidence"],
            }
            sections.append(section)

        return sections
    return [
        paper_lookup,
        author_lookup,
        section_lookup,
    ]
    
