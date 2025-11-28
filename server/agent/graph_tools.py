"""
This file contains the logic for creating a structured representation of the paper’s content, 
such as  paper_title, author, and sections nodes.
"""

from typing import List,Dict
from .graph_config import driver
from neo4j import AsyncSession
import json,re

def parse_str_to_json(text: str):
    match = re.search(r"```json\s*(.*?)```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON block found.")

    json_text = match.group(1).strip()
    data=()

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        # fallback: remove remaining line breaks or carriage returns
        clean_text = json_text.replace("\n", "").replace("\r", "").replace("\t", " ")
        return json.loads(clean_text)

async def build_structured_graph(struct_data: Dict, session_id: str):
    document_title: str = struct_data["document_title"]
    authors: List[Dict] = struct_data["authors"]
    sections: List[Dict] = struct_data["sections"]

    async with driver.session() as session:
        # Create title node
        await create_title_node(document_title, session_id, session)

        # Create authors
        if authors:
            await create_author_nodes(document_title, authors, session_id, session)

        # Create sections
        if sections:
            await create_sections_nodes(document_title, sections, session_id, session)


async def create_title_node(document_title: str, session_id: str, session:AsyncSession):
    query = """
    MERGE (p:Paper {title: $title,session_id:$session_id})
    RETURN p
    """
    await session.execute_write(lambda tx: tx.run(query, title=document_title, session_id=session_id))

    
async def create_author_nodes(document_title: str, authors: list[dict], session_id: str, session:AsyncSession):
    query = """
    UNWIND $authors AS a
    MERGE (auth:Author {name: a.name,session_id:$session_id})
      ON CREATE SET auth.email = a.email, auth.affiliations = a.affiliations
    WITH auth
    MATCH (p:Paper {title: $title})
    MERGE (auth)-[:AUTHORED]->(p)
    """
    await session.execute_write(lambda tx: tx.run(query, authors=authors, title=document_title, session_id=session_id))


async def create_sections_nodes(document_title: str, sections: list[dict], session_id: str, session:AsyncSession):
    query = """
    UNWIND $sections AS s
    MERGE (sec:Section {section_name: s.section_name, section_number: s.section_number,session_id:$session_id})
      ON CREATE SET sec.start_page = s.start_page,
                    sec.confidence = s.confidence,
                    sec.content = s.content
                    
    WITH sec
    MATCH (p:Paper {title: $title,session_id:$session_id})
    MERGE (p)-[:HAS_SECTION]->(sec)
    """
    await session.execute_write(lambda tx: tx.run(query, sections=sections, title=document_title, session_id=session_id))

