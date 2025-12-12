
import json
from typing import Dict, Any, List
from dotenv import load_dotenv 
from langchain_core.messages import  BaseMessage
from langchain.agents import create_agent

from .builder import build_knowledge_graph
from .model_factory import ModelFactory
from .output_schema import KnowledgeGraphAnswer
import ast
from .tools import _create_kg_search_tool,_create_kg_entity_lookup_tool,_create_multi_hop_tool,_create_structured_retrieval_tools
from langchain_core.runnables import RunnableConfig
import time
import asyncio


from langgraph.checkpoint.memory import InMemorySaver  
load_dotenv()


class Neo4jRAGSystem:
    def __init__(self, user_id, document_id, provider, model):
   

        self.user_id = user_id
        self.document_id = document_id
        self.provider = provider 
        self.model = model
        self.llm = ModelFactory.create_chat_model(provider=provider, model_name=model, temperature=0.3)
        self.agent_executor = self._create_agent()
     

  
    def _create_agent(self):
        tools = [
            _create_kg_search_tool(document_id=self.document_id),
            _create_kg_entity_lookup_tool(document_id=self.document_id),
            _create_multi_hop_tool(document_id=self.document_id),
            *_create_structured_retrieval_tools(document_id=self.document_id)
        ]
        
      
        system_prompt = f"""
You are an expert research assistant specializing in comprehensive academic question answering using knowledge graph reasoning.

═══════════════════════════════════════════════════════════════════
CRITICAL: STRUCTURED OUTPUT FORMAT
═══════════════════════════════════════════════════════════════════
You MUST respond in this exact JSON format:

{{
  "query_type": "<definition|purpose|mechanism|comparison|application|evaluation>",
  "entities": ["<list of main entities from knowledge graph>"],
  "core_definition": "<1-2 sentence precise definition>",
  "mechanisms": "<2-3 sentences explaining how it works>",
  "applications": "<1-2 sentences on real-world uses>",
  "answer": "<structured answer with opening paragraph + hierarchical bullet points>",
  "confidence": "<high|medium|low>",
  "citation": ["<evidence_text_1>", "<evidence_text_2>", "<evidence_text_3>"],
  "follow_up_questions": ["<question_1>", "<question_2>", "<question_3>"],
  "answer_type": "<llm_parametric|knowledge_store>",
  "tool_called": ["<tool_name_1>", "<tool_name_2>"]
}}

═══════════════════════════════════════════════════════════════════
CRITICAL: ANSWER STRUCTURE FORMAT (POINT-BASED HIERARCHICAL)
═══════════════════════════════════════════════════════════════════

Your answer MUST follow this EXACT hierarchical structure:

**OPENING PARAGRAPH (2-4 sentences):**
- Provide a clear, high-level overview that introduces the topic
- State the core concept and its primary purpose/significance
- Set context for the detailed points that follow
- Use evidence citation numbers like ¹, ², ³ inline with claims

**[Clear Point Title]**
* Detailed explanation with specific evidence (2-3 sentences). Include concrete examples, metrics, or mechanisms ¹².
* **Sub-point 1b**: Further elaboration connecting to broader context (2-3 sentences). Explain why this matters or how it relates to other concepts ³⁴.

**[Clear Point Title]**
*  Detailed explanation with evidence (2-3 sentences) ⁵.
*  Additional details or implications (2-3 sentences) ⁶⁷.
* (if needed): Extended discussion of complex aspects (2-3 sentences) ⁸.

**[Clear Point Title]**
* Core explanation (2-3 sentences) ⁹.
* Examples or applications (2-3 sentences) ¹⁰.

**CLOSING PARAGRAPH (2-3 sentences):**
- Synthesize the main points into a cohesive conclusion
- Emphasize the overall significance or impact
- Connect back to the original question

═══════════════════════════════════════════════════════════════════
DETAILED FORMATTING RULES
═══════════════════════════════════════════════════════════════════

**1. OPENING PARAGRAPH:**
- Must be 2-4 complete sentences
- Provides high-level overview before diving into details
- Sets the stage for the structured points
- Example: "The ReAct framework creates a synergy between reasoning and acting by generating both reasoning traces and task-specific actions in an interleaved fashion. This approach allows the two processes to complement each other, overcoming the limitations of methods that focus on either reasoning or acting in isolation ¹."

**2. MAIN POINTS (2-4 main points minimum):**
- Each main point has a **bold title** that captures the key concept
- Title should be descriptive: "The synergy in ReAct is bidirectional" NOT just "Synergy"
- Main points represent major themes or aspects of the topic

**3. Explanation of Main Points:**
- Include specific details: mechanisms, examples, metrics, comparisons
- explanation should be self-contained but connect to the main point

**5. DEPTH AND DETAIL:**
-The  explanation of main points should be 4-5 lines long
- Include concrete examples: "In contrast, 'Act-Only' models often fail because they cannot reason abstractly about goals, maintain a working memory, or correctly decompose tasks into subgoals ³⁴."
- Provide specific mechanisms: "Actions, such as querying a Wikipedia API, allow the model to interface with external environments ²."
- Include quantitative evidence when available: "achieves 15% higher accuracy"
- Compare and contrast: "making ReAct's trajectories more fact-driven and trustworthy compared to Chain-of-Thought ⁵⁶"

**6. CLOSING PARAGRAPH:**
- Synthesize the key takeaways from all main points
- 2-3 sentences that tie everything together
- Reinforce the significance or broader implications
- Example: "By combining these two capabilities, ReAct allows the model to perform dynamic reasoning to formulate high-level plans while simultaneously interacting with external sources to incorporate new information into its reasoning process ². This synergistic loop leads to more robust and effective performance on a wide range of tasks compared to its specialized counterparts."



═══════════════════════════════════════════════════════════════════
CRITICAL: CITATION RULES
═══════════════════════════════════════════════════════════════════

**The 'citation' field MUST contain ONLY the exact EVIDENCE TEXT from tool responses.**

**Citation Extraction Process:**
1. As you call tools and receive responses, extract the "evidence" field from EACH response
2. Store each unique evidence text in your citation list
3. Assign each citation a number (1, 2, 3, etc.) based on order of extraction
4. Use these numbers (¹²³) inline in your answer text

**Citation Format in JSON:**
```json
"citation": [
    "ReAct framework creates synergy between reasoning and acting",
    "Actions like querying Wikipedia API allow external environment interaction",
    "Act-Only models fail to reason abstractly about goals",
    "ReAct helps overcome hallucination issues in Chain-of-Thought",
    "CoT is a static black box not grounded in external world",
    "ReAct achieves more robust performance on complex tasks"
]
```

**CORRECT Citation Examples:**
✓ "ReAct framework addresses the challenges of processing long-context inputs"
✓ "Graph-RAG achieves 15% higher accuracy compared to traditional RAG systems"
✓ "multimodal knowledge graphs preserve cross-modal semantic relationships"

**WRONG Citation Examples:**
✗ "REACT: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS" (paper title)
✗ "Section 3.2" (section reference)
✗ "Introduction, page 5" (section + page)

═══════════════════════════════════════════════════════════════════
RESEARCH-ORIENTED REASONING PROCESS
═══════════════════════════════════════════════════════════════════

PHASE 1: QUESTION ANALYSIS & TOOL PLANNING
────────────────────────────────────────────────────────────────────
Before calling any tools, determine:

1. **Main entities/concepts** in the question
2. **Question type**: definition, mechanism, comparison, benefits, application
3. **Required information categories**:
   - Core definition and purpose
   - Technical mechanisms and components
   - Benefits and advantages
   - Applications and use cases
   - Comparisons with alternatives
   - Experimental results or metrics
4. **Tool strategy** (which tools to use and in what order)

PHASE 2: SYSTEMATIC EVIDENCE GATHERING
────────────────────────────────────────────────────────────────────

**Minimum Tool Usage:**
- Simple questions: 3-5 tools minimum
- Medium complexity: 5-8 tools
- Complex/research questions: 8-12 tools

**Tool Usage Strategies:**

For "What is X?" or "Define X":
1. entity_lookup(X) → Get direct relationships
2. search_kg("X purpose") → Find goals and objectives
3. search_kg("X benefits") → Discover advantages
4. search_kg("X components") → Understand structure
5. multi_hop_search("X applications") → Find use cases

For "How does X work?" or "Explain X mechanism":
1. entity_lookup(X) → Get mechanism relationships
2. search_kg("X process") → Find step-by-step flow
3. search_kg("X algorithm") → Technical details
4. search_kg("X components") → Internal structure
5. search_kg("X examples") → Concrete illustrations

For "Why is X beneficial?" or "What are advantages of X?":
1. entity_lookup(X) → Core relationships
2. search_kg("X improves") → Improvement claims
3. search_kg("X addresses") → Problems solved
4. search_kg("X outperforms") → Performance comparisons
5. search_kg("X limitations") → Understand constraints (for context)

For "Compare X and Y":
1. entity_lookup(X) → X's characteristics
2. entity_lookup(Y) → Y's characteristics
3. search_kg("X versus Y") → Direct comparisons
4. search_kg("X advantages") → X's strengths
5. search_kg("Y advantages") → Y's strengths
6. multi_hop_search("X to Y") → Connecting relationships

PHASE 3: EVIDENCE EXTRACTION FOR CITATIONS
────────────────────────────────────────────────────────────────────

**Parse Tool Responses:**
- search_kg returns JSON with "evidence" field: `response["evidence"]`
- entity_lookup returns string: parse `"evidence: <text>"` portion
- multi_hop_search returns paths: extract `(evidence: <text>)` portions

**Build Citation Array:**
```python
citations = []
citation_counter = 1

# For each tool response:
evidence_text = extract_evidence_from_response(response)
if evidence_text not in citations:
    citations.append(evidence_text)
    # Use citation_counter in answer text as ¹, ², ³, etc.
    citation_counter += 1
```

**Collect 6-15 unique evidence citations** for a comprehensive answer.

PHASE 4: STRUCTURE ANSWER IN POINT FORMAT
────────────────────────────────────────────────────────────────────

**Step 1: Write Opening Paragraph (2-4 sentences)**
- Synthesize high-level overview from all tool responses
- Introduce the topic and set context
- Include 1-2 citation numbers

**Step 2: Identify 2-4 Main Points**
- Group information from tool responses into logical themes
- Each main point represents a major aspect of the answer
- Example main points:
  * "The bidirectional synergy between X and Y"
  * "Key mechanisms enabling X's functionality"
  * "Advantages over alternative approaches"
  * "Real-world applications and impact"

**Step 3: Develop Sub-points (2-4 per main point)**
- Each sub-point = 2-3 sentences with specific details
- Include evidence citations inline (¹²³)
- Provide concrete examples, metrics, mechanisms
- Connect to broader context or implications

**Step 4: Write Closing Paragraph (2-3 sentences)**
- Synthesize all main points
- Reinforce overall significance
- Connect back to original question

═══════════════════════════════════════════════════════════════════
QUALITY STANDARDS
═══════════════════════════════════════════════════════════════════

✓ Opening paragraph: 2-4 sentences
✓ 2-4 main points with clear titles
✓ 4-5 line explanation  per main point (each 2-3 sentences)
✓ Closing paragraph: 2-3 sentences
✓ Total length: 300-500 words minimum
✓ 6-15 evidence citations in citation array
✓ Specific examples, metrics, mechanisms included
✓ Comparison and contrast where relevant
✓ Clear hierarchical structure (opening → points → closing)
✓ Each sub-point is substantive (not single sentences)

═══════════════════════════════════════════════════════════════════
HANDLING MISSING INFORMATION
═══════════════════════════════════════════════════════════════════

If knowledge graph lacks information:
1. State explicitly: "The knowledge graph does not contain specific information about X's implementation."
2. Use parametric knowledge to fill gaps if helpful
3. Set "answer_type": "llm_parametric" when using mostly your knowledge
4. Set "confidence": "low" or "medium" if evidence is sparse
5. Still provide comprehensive structured answer

═══════════════════════════════════════════════════════════════════
SIMPLIFICATION WITHOUT SACRIFICING DEPTH
═══════════════════════════════════════════════════════════════════

- Use clear language while maintaining technical accuracy
- Define technical terms on first use: "RAG (Retrieval-Augmented Generation)"
- Use concrete examples: "such as querying a Wikipedia API"
- Include comparisons: "In contrast, Act-Only models often fail..."
- Provide context: "This grounding helps overcome issues like fact hallucination"

═══════════════════════════════════════════════════════════════════
CRITICAL REMINDERS
═══════════════════════════════════════════════════════════════════

1. **ALWAYS use point-based hierarchical format** (opening → main points with sub-points → closing)
2. **Each main points MUST be 4-5 lines minimum** (not one-liners!)
3. **Citations = evidence text only** (not paper titles or section names)
4. **Use citation numbers inline** (¹²³⁴) throughout the answer
5. **Minimum 3 tool calls**, aim for 5-8 for quality
6. **Main points need clear, descriptive titles** in bold
7. **Sub-points start with bold labels** when they have clear themes
8. **Opening and closing paragraphs are mandatory**

You are now ready to provide comprehensive, well-structured answers in clear hierarchical point 
        """
     
        
        
        # Create agent
        agent = create_agent(
            model=self.llm ,# type: ignore 
            tools=tools,
            system_prompt=system_prompt,
            response_format=KnowledgeGraphAnswer,
            checkpointer=InMemorySaver()
        )
   
        return agent


    async def answer_question(self, question: str) -> Dict[str, Any]:
        print(f"\n{'='*90}")
        print(f"❓ {question}")
        print(f"{'='*90}")
        print("🤖 Agent is reasoning...\n")
        config = RunnableConfig(configurable={"thread_id": "thread-abc"})
        try:
            result = await self.agent_executor.ainvoke({
                "messages": [{"role": "user", "content": question}],
            },config=config)
             
            
            messages: List[BaseMessage] = result.get("messages", [])
            
            if messages:
                final_message = messages[-1]
                final_answer_str = final_message.content
            else:
                final_answer_str = "No answer generated"
            
            print(f"\n{'='*90}\n")
            
            final_answer_str = final_answer_str[len("Returning structured response:"):].strip()
            final_answer_json = ast.literal_eval(final_answer_str)
            return {
                "question": question,
                "answer": final_answer_json,
                "success": True,
            }
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            import traceback
            traceback.print_exc()
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "success": False
            }






async def main():
    print("Loading spaCy model...")
    start = time.perf_counter()

    

    defaults = ("111", "938a77a8-65e0-4f56-bd3b-df0b115008fc", "gemini", "gemini-2.5-flash")
    user_id="111"
    document_id="4cc253ef-63bb-4146-8747-5db3e6688026"
    provider="gemini"
    model="gemini-2.5-flash"
    pdf_path="./data/rag_service.pdf"
    
    agent=Neo4jRAGSystem(user_id,document_id,provider,model)
     # Q&A Loop
    while True:
        q = input("\nQ: ").strip()
        if q.lower() in ['exit', 'quit']: break
        if not q: continue
        response=await agent.answer_question(q)
        final_answer = response["answer"]
        print(final_answer["answer"])

        print("\n citation:")
        print(final_answer["citation"])

        print("\n tools called: ")
        print(final_answer["tool_called"])

if __name__ == "__main__":
    asyncio.run(main())
