"""
File contains:
    -class for extracting entity and relationship from plain texts.
    -extraction will be done depending using nlp library and llm.
    - if sentences are below 5000 character then llm extraction will be appended with manual extraction.
"""
import re
from typing import Dict,List,Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
from .model_factory import ModelFactory
import asyncio

class Entity_Relation_Extractor:
    """Extract high-quality relationships with proper relations"""
    
    def __init__(self, nlp_model, use_llm: bool = True,provider:str="gemini",model:str="gemini-2.5-flash"):
        self.nlp = nlp_model
        self.use_llm = use_llm
        self.llm = None
        try:
            self.llm = ModelFactory.create_chat_model(provider,model,0.3)
            print("✓ LLM initialized for extraction\n")
        except Exception as e:
            print(f"LLM not available: {e}\n")
    
    async def extract_from_text(self, text: str) -> List[Dict[str,Any]]:
        """Extract relationships from text with proper cleaning"""
        print("Extracting relationships...")
        
        # Clean text first
        text = self._clean_text(text)
        
        
        all_triples = []
        print("Using LLM for enhanced extraction...")
        llm_triples = await self._extract_with_llm_async(text)
        all_triples.extend(llm_triples)
        
        # Post-process
        processed = self._post_process(all_triples)
        
        print(f"✓ Extracted {len(processed)} high-quality relationships\n")
        return processed
    
    def _clean_text(self, text: str) -> str:
        """Clean text before processing"""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix concatenated words (common PDF issue)
        # e.g., "fragmentationthroughaunifiedgraph" -> "fragmentation through a unified graph"
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        # Add spaces around common conjunctions if missing
        text = re.sub(r'(\w)(through|based|with|from|into|onto|across)(\w)', 
                     r'\1 \2 \3', text, flags=re.IGNORECASE)
        
        # Fix "aunified" -> "a unified"
        text = re.sub(r'\ba(\w)', r'a \1', text)
        
        # Remove special characters that break parsing
        text = re.sub(r'[^\w\s\.\,\;\:\-\'\"\(\)]', ' ', text)
        
        # Normalize punctuation spacing
        text = re.sub(r'\s+([.,;:])', r'\1', text)
        text = re.sub(r'([.,;:])\s+', r'\1 ', text)
        
        return text.strip()
    
    def _chunk_text(self, text: str, max_length: int,max_chunks:int=10,min_chunk_size:int=1000) -> List[str]:
        """Split text into chunks""" 
        text_length=len(text)
        chunk_size=max(min_chunk_size,text_length // max_chunks)

        overlap=min(500,int(chunk_size * 0.1))
        splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap,
                separators=["\n\n","\n",""," "],
                is_separator_regex=False,
                )
        chunks = splitter.split_text(text)
        while len(chunks) > max_chunks:
            # Merge last two chunks
            chunks[-2] = chunks[-2] + chunks[-1]
            chunks.pop()

        return chunks


    
    def _extract_structure_with_llm(self,text:str)->str:
        
        if not self.llm:
          return ""
        section_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", '''You are an expert at analyzing academic paper structure and extracting ONLY the most important sections.

**CRITICAL JSON FORMATTING RULES:**
1. ALL string values MUST escape special characters:
   - Replace " with \\" (!strictly follow this format or else code will break)
2. NO trailing commas after last array element
3. NO comments or text outside the JSON structure
4. Use only plain ASCII quotes (") in all JSON keys and values

**EXTRACT ONLY THESE CRITICAL SECTIONS (in order of priority):**

**REQUIRED SECTIONS (must extract if present):**
1. **Abstract** - Paper summary at the beginning
2. **Introduction** - Problem statement, motivation, contributions
3. **Methodology / Method / Approach** - How the research was conducted
4. **Results / Experiments / Evaluation** - What was found/measured
5. **Conclusion / Discussion** - Summary and implications
6. **Related Work / Background / Literature Review** - Prior research context

**OPTIONAL SECTIONS (extract if significant):**
7. **Motivation** - Why this research matters (if separate from intro)
8. **Findings / Contributions** - Key discoveries (if not in results)

**DO NOT EXTRACT:**
- References/Bibliography (skip entirely)
- Acknowledgments
- Appendices
- Supplementary materials
- Author bios
- Detailed subsections (like 3.1, 3.2, 4.1, etc.) - merge into parent section
- Tables and Figures (skip or briefly mention in parent section)

**Section Merging Rules:**
- If a paper has "3. Methodology", "3.1 Dataset", "3.2 Model Architecture", extract ONLY the parent "3. Methodology" with all subsection content combined
- Merge all subsections into their parent section
- Example: "4. Results", "4.1 Quantitative Results", "4.2 Qualitative Analysis" → Extract as single "Results" section

**Input Format:**
The text contains:
1. Page markers: `{{PAGE X}}`
2. Category markers: `===[CategoryName]===` (e.g., `===[Title]===`, `===[NarrativeText]===`)

**Section Identification:**
- Look for `===[Title]===` markers with section keywords
- Match against the required section names (case-insensitive)
- Sections often appear after page breaks
- Roman numerals (I., II., III.) or numbers (1., 2., 3.) indicate major sections

**Content Extraction Rules:**
- For REQUIRED sections: Extract COMPLETE, FULL content (no summarization)
- Include all text from section start until next major section begins
- Preserve technical details, equations, citations
- Keep original formatting and paragraph structure

**Output Format:**
Return a JSON object with ONLY the important sections found:

```json
{{
  "document_title": "extracted title of the paper",
  "authors": [
    {{
      "name": "Author Name",
      "affiliations": ["Institution"],
      "email": "email@domain.edu"
    }}
  ],
  "sections": [
    {{
      "section_name": "Abstract",
      "section_number": "NAN",
      "start_page": 1,
      "confidence": "high",
      "content": "[FULL TEXT - all content from abstract]",
      "content_type": "main_section"
    }},
    {{
      "section_name": "Introduction",
      "section_number": "1",
      "start_page": 1,
      "confidence": "high",
      "content": "[FULL TEXT - complete introduction including all subsections]",
      "content_type": "main_section"
    }},
    {{
      "section_name": "Methodology",
      "section_number": "3",
      "start_page": 4,
      "confidence": "high",
      "content": "[FULL TEXT - entire methodology section with all 3.1, 3.2, etc. merged]",
      "content_type": "main_section"
    }},
    {{
      "section_name": "Results",
      "section_number": "4",
      "start_page": 7,
      "confidence": "high",
      "content": "[FULL TEXT - all experimental results and evaluations]",
      "content_type": "main_section"
    }},
    {{
      "section_name": "Conclusion",
      "section_number": "5",
      "start_page": 10,
      "confidence": "high",
      "content": "[FULL TEXT - complete conclusion and discussion]",
      "content_type": "main_section"
    }}
  ]
}}
```

**Expected Output Size:**
- Typical academic paper should return 4-6 sections
- Minimum: Abstract, Introduction, Methodology, Conclusion
- Maximum: 8 sections (if paper has all optional sections)

**Quality Check:**
Before returning, verify:
1. ✓ Only major sections extracted (no subsections like 3.1, 4.2)
2. ✓ No References/Acknowledgments sections
3. ✓ Each section has full content (not truncated)
4. ✓ Valid JSON syntax (no trailing commas, proper escaping)
5. ✓ Section count is between 4-8

REMEMBER: Quality over quantity. 5 well-extracted important sections is better than 30 sections with everything included.
'''),
    ("user", "{text}")
])


        
        chain=section_extraction_prompt | self.llm 
        response=chain.invoke({"text":text})

        return str(response.content)
    
    def _clean_entity(self, text: str) -> str:
        """Clean and normalize entity"""
        if not text:
            return ""
        
        # Strip whitespace and punctuation
        text = text.strip()
        text = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', text)
        
        # Remove articles
        text = re.sub(r'^(a|an|the)\s+', '', text, flags=re.IGNORECASE)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Capitalize properly
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]
        
        return text.strip()
    
    def _is_valid_triple(self, subject: str, relation: str, obj: str) -> bool:
        """Validate triple quality"""
        # Check existence
        if not all([subject, relation, obj]):
            return False
        
        # Check minimum length
        if len(subject) < 2 or len(obj) < 2 or len(relation) < 2:
            return False
        
        # Subject and object must be different
        if subject.lower() == obj.lower():
            return False
        
        # Avoid vague terms
        vague = {'it', 'this', 'that', 'these', 'those', 'thing', 'stuff', 
                 'something', 'anything', 'everything', 'nothing'}
        
        if subject.lower() in vague or obj.lower() in vague:
            return False
        
        # Avoid very long entities (likely parsing errors)
        if len(subject) > 100 or len(obj) > 100:
            return False
        
        # Avoid entities with too many words (likely sentence fragments)
        if len(subject.split()) > 8 or len(obj.split()) > 8:
            return False
        
        return True
    
    def _post_process(self, triples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and deduplicate triples"""

        seen = set()
        unique = []
        
        for triple in triples:
            subj = triple["subject"]
            rel = triple["relation"]
            obj = triple["object"]
            
            key = (subj.lower(), rel.lower(), obj.lower())
            if key not in seen:
                seen.add(key)
                unique.append(triple) 
        
        return unique

    async def _extract_with_llm_async(self, text: str) -> List[Dict[str, Any]]:
      """Use LLM for high-quality extraction with async parallel processing"""
      if not self.llm:
          print("=== No LLM initialized ===")
          return []
      
      chunks = self._chunk_text(text, 5500)
      
      # Reduce chunk processing if needed
      chunks_to_process = chunks[:10]
      
      prompt = ChatPromptTemplate.from_messages([
                ("system", """
You are an expert knowledge graph engineer extracting precise, formal relationships from academic and technical documents with SOURCE ATTRIBUTION.

**CRITICAL JSON FORMATTING RULES:**
1. Escape special characters: " → \\"  \\n → \\n  \\t → \\t
2. NO trailing commas after last array element
3. NO comments outside JSON structure
4. Evidence must be single line (no line breaks)
5. Use only plain ASCII quotes (") in all JSON keys and values

**ENTITY TYPE CLASSIFICATION:**
- Formal_Definition: Mathematical or formally defined constructs, formulas, or symbolic expressions (e.g., A^ = A ∪ L)
- Concept: High-level ideas or methods (e.g., ReAct reasoning-acting framework)
- Algorithm: Step-by-step procedures (e.g., Graph-RAG algorithm)
- Metric: Evaluation measures or benchmarks
- Task: Specific datasets or problem domains (e.g., HotpotQA, ALFWorld)
- Component: Technical building blocks (e.g., action space, reasoning module)

**FORMALITY LEVELS:**
- mathematical: Contains equations or symbols (∪, ∈, =, ∑, α, β)
- formal: Precise technical definition without math notation
- conceptual: High-level description

**EXTRACTION RULES:**
1. Identify **formal definitions**: Phrases like "we define," "formally," "let X be," "X is defined as," "A^ = A ∪ L"
2. Extract **symbolic notation** into the "formal_notation" field
3. Extract relationships that explain **who does what to whom**, including:
   - Causal: X enables Y, X addresses Y
   - Compositional: X consists_of Y, X includes Y
   - Purpose: X is_designed_for Y, X aims_to Y
   - Comparison: X outperforms Y
   - Quantitative: X improves Y_by Z%
4. Use **page markers** ({{{{PAGE X}}}}) for evidence attribution; default to page 1 if missing
5. Include **10-30 high-quality triples**, prioritizing:
   - Formal definitions
   - Technical components and architectures
   - Core algorithms and task interactions
   - Quantitative or symbolic relations
6. Avoid vague entities, pronouns, meta-statements, or trivial claims

**OUTPUT FORMAT:**
{{
  "triples": [
    {{
      "subject": "entity1",
      "subject_type": "Formal_Definition|Concept|Algorithm|Metric|Task|Component",
      "relation": "descriptive_action_verb",
      "object": "entity2",
      "object_type": "Formal_Definition|Concept|Algorithm|Metric|Task|Component",
      "evidence": "exact text span from document (20-200 chars)",
      "formality_level": "mathematical|formal|conceptual",
      "page": page_number | "NAN",
      "confidence": "high|medium|low"
    }}
  ]
}}

**EXTRACTION STRATEGY:**
- If a formal definition is detected, set `subject_type` or `object_type` to Formal_Definition, `formal_notation` to the symbolic expression, and `formality_level` to mathematical.
- Capture **reasoning-action separation** in frameworks like ReAct (e.g., augmented action space A^, dense vs sparse thoughts)
- Capture **task-specific adaptations**: How components or algorithms interact with tasks (HotpotQA, ALFWorld)
- Include **internal mechanisms** (e.g., planning, reflection, error recovery) as distinct triples
- Preserve **symbolic notation, formulas, and equations** even if partially corrupted by PDF extraction

Return ONLY a valid JSON object with the `triples` array. No markdown, no explanation.
"""),
                ("human", """Extract knowledge graph triples from this text with source attribution.

The text contains {{{{PAGE X}}}} markers indicating page boundaries. Use these to accurately set the "page" field for each triple.

Text:
{text}

Return ONLY the JSON object with triples array (no markdown, no explanation):""")
            ])
      
      async def process_chunk(chunk: str) -> List[Dict[str, Any]]:
          """Process a single chunk asynchronously"""
          chunk_triples = []  # Initialize here, not after try
          try:
              chain = prompt | self.llm # type: ignore
                
              print("calling api .....")
              response = await chain.ainvoke({"text": chunk})
              
              content = str(response.content).strip()
              
              print(content)
              # Remove markdown
              if "```json" in content:
                  content = content.split("```json")[1].split("```")[0]
              elif "```" in content:
                  content = content.split("```")[1].split("```")[0]
              
              # Parse JSON
              triples_data = json.loads(content)
          

              if isinstance(triples_data, dict) and "triples" in triples_data:
                    for triple in triples_data["triples"]:
                        # Clean entities carefully
                        sub = self._clean_entity(triple.get("subject", ""))
                        obj = self._clean_entity(triple.get("object", ""))
                        
                        # Relation normalization
                        rel = triple.get("relation", "")
                        if rel:
                            rel = "_".join(rel.strip().split()).lower()  # spaces → underscores

                        # Escape JSON special characters in evidence
                        evidence = triple.get("evidence", "")
                        evidence = evidence.replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
                        
                        # Default values for new fields
                        sub_type = triple.get("subject_type", "Concept")
                        obj_type = triple.get("object_type", "Concept")
                        formality = triple.get("formality_level", "conceptual")
                        page = triple.get("page", "NAN")
                        confidence = triple.get("confidence", "medium")

                        # Only append valid triples
                        if self._is_valid_triple(sub, rel, obj):
                            chunk_triples.append({
                                "subject": sub,
                                "subject_type": sub_type,
                                "relation": rel,
                                "object": obj,
                                "object_type": obj_type,
                                "evidence": evidence,
                                "formality_level": formality,
                                "page": page,
                                "confidence": confidence
                            })
                     
              return chunk_triples  # Return the list we built
              
          except Exception as e:
              print(f"   LLM chunk error: {e}")
              return []  # Return empty list on error
            # Process all chunks in parallel
   
      results = await asyncio.gather(*[process_chunk(chunk) for chunk in chunks_to_process])
      
      # Flatten results
      all_triples = [triple for chunk_result in results for triple in chunk_result]
      
      print(all_triples)
      return all_triples
