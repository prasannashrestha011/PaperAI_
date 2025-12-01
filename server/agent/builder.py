"""
File contains:
 -text extractor from pdf  
 -knowledge graph builder handler
"""

import spacy

from unstructured.partition.pdf import partition_pdf
from server.agent.graph_store import kg_store
from .extractor import Entity_Relation_Extractor
import requests
from io import BytesIO
from .graph_tools import parse_str_to_json
from .graph_tools import build_structured_graph
import os
import time



def clean_text(text: str) -> str:
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return text

def extract_text_from_pdf(url: str, quality: str) -> str:
    """Extraction using unstructured: returns a single string with page markers"""
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()  
    pdf_bytes = response.content
    pdf_file_like = BytesIO(pdf_bytes)
    elements = partition_pdf(
        file=pdf_file_like,
        strategy="hi_res" if quality == "H" else "fast",
        infer_table_structure=True if quality == "H" else False,
        languages=['english']  
    )
    pages = {}
    # Group text by page
    for el in elements:
        if hasattr(el, "text") and el.text.strip():
            page = getattr(el.metadata, "page_number", 0)
            pages.setdefault(page, []).append((el.category, el.text.strip()))

    # Combine each page into a single string with page marker
    all_text = ""
    for page, items in sorted(pages.items()):
        all_text += f"{{PAGE {page}}}\\n"
        for category, text in items:
            cleaned_text = clean_text(text)  # clean each text block
            all_text += f"[{category}] {cleaned_text}\\n"
        all_text += "\\n"

    return all_text




async def build_knowledge_graph(pdf_path: str,document_id:str,provider:str,model:str,quality:str):
    """Build knowledge graph from PDF"""

    nlp = spacy.load("en_core_web_sm")
    print(f"Reading: {pdf_path}")
    start=time.perf_counter()
    text = extract_text_from_pdf(pdf_path,quality)
    end=time.perf_counter()

  
  
    print(f"✓ Extracted {len(text):,} characters\n")
    # Extract relationships
    extractor = Entity_Relation_Extractor(nlp_model=nlp, use_llm=True,provider=provider,model=model)
    

    s_start=time.perf_counter()
    structure=extractor._extract_structure_with_llm(text)
    s_end=time.perf_counter()
    print(f"Structure data extraction time: {s_end-s_start:.4f}")

    print(structure)
    struct_data=parse_str_to_json(structure)
    await build_structured_graph(struct_data,document_id)

    triples = await extractor.extract_from_text(text)
    await kg_store.store_triples_batch(document_id,triples, os.path.basename(pdf_path))

    print(f"PDF extraction time: {end-start:.4f} seconds ")


    """
    print(structure)
    if not structure:
        print("Failed to fetch the structured data")
        return
    
    """
    
    # Store
   

    return kg_store

