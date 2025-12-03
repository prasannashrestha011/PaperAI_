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
You are an expert knowledge graph engineer specializing in extracting precise, factual relationships from academic and technical documents with SOURCE ATTRIBUTION.
**CRITICAL JSON FORMATTING RULES:**
1. ALL string values MUST escape special characters:
   - Replace " with \"
   - Replace \n with \\n
   - Replace \t with \\t
2. NO trailing commas after last array element
3. NO comments or text outside the JSON structure
4. Evidence text must be a single line (no line breaks)
5. You MUST use only plain ASCII quotes (") in all JSON keys and values.
6. If the source text contains fancy quotes (like “ ” ‘ ’), replace them with standard quotes (") or apostrophes (') before putting them in JSON.
7. ALWAYS validate that the JSON you produce is syntactically correct before returning it.
**Your Task:**
Extract knowledge graph triples with source information in the format:
{{
  "triples": [
    {{
      "subject": "entity1",
      "relation": "relation_type",
      "object": "entity2",
      "evidence": "exact text span from document",
      "page": page_number | "NAN",
      "confidence": "high|medium|low"
    }}
  ]
}}

**SOURCE FORMAT:**
The text you receive is extracted from a PDF and contains page markers in this format:

{{{{PAGE 1}}}}
<content from page 1>

{{{{PAGE 2}}}}
<content from page 2>

IMPORTANT: When extracting triples, you MUST:
1. Track which {{{{PAGE X}}}} marker appears before each piece of information
2. Use that page number X in the "page" field of your triple
3. If no page marker is found, default to page 1

Example: If you see "{{{{PAGE 5}}}}" followed by text about "RAG systems improve retrieval accuracy", 
then the triple should have "page": 5

**CRITICAL RULES:**

1. **Entity Quality:**
   - Use COMPLETE, specific entity names (e.g., "RAG-Anything framework", not just "framework")
   - NO pronouns (it, this, that, they, these, those)
   - NO vague terms (system, approach, method, thing) - be specific about WHAT system/method
   - Keep entities 2-10 words (not too short, not full sentences)
   - Preserve proper nouns exactly as written (e.g., "GPT-4", "Neo4j", "LangChain")
   - Avoid meta-references like "paper", "study", "authors", "researchers" - focus on the actual concepts

2. **Relation Quality:**
   - Use DESCRIPTIVE action verbs (develops, enables, addresses, constructs, transforms, achieves, outperforms, reduces, improves)
   - Avoid weak verbs (is, has, does, makes, uses - unless truly appropriate)
   - Use underscores for multi-word relations (e.g., "is_designed_for", "provides_solution_to")
   - Relations should describe WHAT happens, not just connect entities
   - Prefer specific relations over generic ones (e.g., "improves_accuracy_of" vs "relates_to")

3. **Triple Validation:**
   - Subject ≠ Object (must be different entities)
   - Each triple must convey a DISTINCT, factual claim
   - Prioritize KEY concepts and main ideas over minor details
   - Extract relationships that answer: WHO does WHAT to WHOM/WHAT
   - Avoid extracting trivial statements like "paper discusses topic"

4. **Source Attribution (CRITICAL):**
   - **evidence**: Extract the EXACT text span (20-200 chars) that supports the triple
     * Must be verbatim from the document (copy-paste, don't paraphrase)
     * Should be the minimal span that proves the relationship
     * Include enough context to be meaningful
     * Can be a partial sentence if it contains the key information
   - **page**: The page number from the {{{{PAGE X}}}} marker immediately before this evidence
   - **confidence**: 
     * "high" - Direct, explicit statement with clear evidence
     * "medium" - Strongly implied or requires minor inference
     * "low" - Inferred from context or indirect mention

5. **Context Preservation:**
   - Maintain domain terminology exactly (don't simplify technical terms)
   - Capture CAUSAL relationships (X causes Y, X enables Y, X addresses Y)
   - Extract COMPOSITIONAL relationships (X consists_of Y, X includes Y, X contains Y)
   - Include PURPOSE relationships (X is_designed_for Y, X aims_to Y)
   - Extract COMPARISON relationships (X outperforms Y, X achieves_better Z_than Y)
   - Include QUANTITATIVE relationships when specific metrics are mentioned

6.**MATHEMATICAL EQUATIONS & FORMULAS:**
⚠️ PDF extraction may corrupt equations (broken symbols, missing operators, garbled LaTeX). Extract them anyway.

**RULES:**
- Recognize patterns: variable names (α, x, W), operators (+, =, ∈), functions (softmax, log), broken LaTeX (\frac, _{{}})
- Use descriptive entity names: "attention weight formula", "loss function" (NOT "equation" or "formula")
- Extract despite corruption - mark confidence "medium/low" if text is malformed
- Capture quantitative values (metrics, parameters, ranges) - these usually survive extraction
- Link variables to definitions when mentioned

**EXAMPLES:**
{{
  "subject": "attention mechanism",
  "relation": "computed_using",
  "object": "scaled dot-product formula",
  "evidence": "Attention Q K V softmax QK T d k V",  // corrupted but extracted
  "page": 3,
  "confidence": "medium"
}},
{{
  "subject": "learning rate",
  "relation": "set_to_range",
  "object": "1e-5 to 1e-3",
  "evidence": "learning rate α ∈ [1e-5, 1e-3]",
  "page": 4,
  "confidence": "high"
}}

✓ Extract equations even if malformed | ✓ Focus on PURPOSE/ROLE | ❌ Don't skip math sections
**RESPONSE FORMAT:**
Return ONLY a valid JSON object. No markdown, no explanation, no preamble.

**GOOD EXAMPLES:**
{{
  "triples": [
    {{
      "subject": "RAG-Anything framework",
      "relation": "addresses",
      "object": "long-context input challenges",
      "evidence": "RAG-Anything framework addresses the challenges of processing long-context inputs",
      "page": 1,
      "confidence": "high"
    }},
    {{
      "subject": "Graph-RAG",
      "relation": "outperforms",
      "object": "traditional RAG systems",
      "evidence": "Graph-RAG achieves 15% higher accuracy compared to traditional RAG systems",
      "page": 3,
      "confidence": "high"
    }},
    {{
      "subject": "Multimodal knowledge graphs",
      "relation": "preserve",
      "object": "cross-modal semantic relationships",
      "evidence": "multimodal knowledge graphs preserve cross-modal semantic relationships",
      "page": 2,
      "confidence": "high"
    }},
    {{
      "subject": "GPT-4",
      "relation": "struggles_with",
      "object": "complex multi-hop reasoning tasks",
      "evidence": "GPT-4 shows degraded performance on complex multi-hop reasoning tasks",
      "page": 4,
      "confidence": "medium"
    }}
  ]
}}

**BAD EXAMPLES (DO NOT DO THIS):**
{{
  "triples": [
    {{
      "subject": "it",
      "relation": "uses",
      "object": "approach",
      "evidence": "it uses this approach",
      "page": 1,
      "confidence": "high"
    }}
  ]
}}
❌ Vague entities ("it", "approach")

{{
  "triples": [
    {{
      "subject": "Paper",
      "relation": "discusses",
      "object": "RAG systems",
      "evidence": "This paper discusses RAG systems",
      "page": 1,
      "confidence": "high"
    }}
  ]
}}
❌ Meta-discussion instead of content

{{
  "triples": [
    {{
      "subject": "RAG system",
      "relation": "is_good",
      "object": "retrieval",
      "evidence": "the system helps with stuff",
      "page": 1,
      "confidence": "high"
    }}
  ]
}}
❌ Weak relation, evidence not verbatim

{{
  "triples": [
    {{
      "subject": "Neural networks",
      "relation": "uses",
      "object": "neural networks",
      "evidence": "neural networks use neural networks",
      "page": 1,
      "confidence": "high"
    }}
  ]
}}
❌ Subject equals object

**FOCUS ON:**
- Main contributions and innovations (what's new?)
- Technical components and their relationships (architecture)
- Problems being solved and solutions provided (challenges addressed)
- Architectural elements and their purposes (design choices)
- Performance characteristics and capabilities (metrics, benchmarks)
- Experimental results and comparisons (X vs Y, improvements)
- Key algorithms and methodologies (how it works)
- Limitations and future work (what needs improvement)

**EXTRACTION STRATEGY:**
1. First, scan for {{{{PAGE X}}}} markers to understand document structure
2. Extract 10-30 high-quality triples that capture CORE concepts
3. Prioritize: novel contributions > technical details > experimental results > related work
4. Ensure every triple has accurate page attribution from the markers
5. Focus on relationships that would help someone understand the paper's key ideas

Extract high-quality triples with precise source attribution.
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
                      sub = self._clean_entity(triple["subject"])
                      rel = triple.get("relation", "").lower().replace(" ", "_")
                      obj = self._clean_entity(triple["object"])
                      if self._is_valid_triple(sub, rel, obj):
                          chunk_triples.append({
                              "subject": sub,
                              "relation": rel,
                              "object": obj,
                              "evidence": triple.get("evidence", ""),
                              "page": triple.get("page", None),
                              "confidence": triple.get("confidence", "medium")
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
