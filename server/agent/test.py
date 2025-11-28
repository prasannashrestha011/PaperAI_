from .graph_config import driver
import asyncio
import spacy  
from langchain_core.documents import Document
nlp_model = spacy.load("en_core_web_sm")
async def author_lookup():
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
                MATCH (a:Author)-[AUTHORED]->(p:Paper {session_id:$session_id})
                RETURN a as author
             """
        async with driver.session() as session:
            results = await session.run(query, session_id="111-111")
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
        print(authors)
        return authors
asyncio.run(author_lookup())
