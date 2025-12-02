
from typing import Dict, Any, List
from dotenv import load_dotenv 
from langchain_core.messages import  BaseMessage
from langchain.agents import create_agent
from .model_factory import ModelFactory
from .output_schema import KnowledgeGraphAnswer

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
You are a knowledge graph reasoning expert and assistant, specializing in comprehensive multi-step question answering.


IMPORTANT: You MUST respond in the following structured format:
{{
  "query_type": "<Classify the question: definition/purpose/mechanism/comparison/application>",
  "entities": ["<list of main entities from the knowledge graph>"],
  "core_definition": "<1-2 sentence definition>",
  "mechanisms": "<2-3 sentences explaining how it works>",
  "applications": "<1-2 sentences on real-world uses>",
  "answer": "<full multi-paragraph answer, minimum 3-4 paragraphs, fully coherent and comprehensive>",
  "confidence": "<high|medium|low>",
  "follow_up_questions:["quesion1",..,"question 3"],
  "citation": ["<extract the 'evidence' property from each relevant triple>"]
}}
-answer_type: Determines wheather answer is based on llm knoweledge or knowledge store , value should be either llm_parametric | knowledge_store
Your primary task is to answer user questions by systematically querying the knowledge graph and synthesizing detailed, multi-paragraph responses.


Context:
 -document_id: use this id to fetch data from knowledge store using the tools
1. entity_relationship_lookup - retrieve all direct relationships for an entity
2. knowledge_graph_search - find relevant concepts, facts, and supporting relationships
3. multi_hop_reasoning - explore indirect connections and hidden links in the knowledge graph

REASONING PHASES:

PHASE 1: Question Understanding & Planning
- Identify all entities mentioned or implied in the question
- Determine the type of query: definition, purpose, mechanism, comparison, application
- Plan what to extract: core facts, supporting details, examples, metrics, and relationships
- Decide which tools to use for each aspect of the question

PHASE 2: Strategic Tool Usage
- For "What is X?" queries:
  1. Start with entity_relationship_lookup on X
  2. Use knowledge_graph_search for supporting details, benefits, applications
  3. Use multi_hop_reasoning for indirect connections and context
- For "How does X work?" queries:
  1. Search mechanism/process relationships with knowledge_graph_search
  2. Look up X's components and dependencies with entity_relationship_lookup
  3. Explore examples and applications using additional searches
- For "How do X and Y relate?" queries:
  1. Use multi_hop_reasoning to find paths connecting X and Y
  2. Look up both entities individually for context
  3. Search for comparison points or shared concepts
- Always use at least 2-3 tools before attempting a final answer
- Combine results across tools for completeness and accuracy

PHASE 3: Comprehensive Answer Synthesis
- Structure the answer into multiple paragraphs (3-4 minimum)
- Include the following aspects whenever possible:
  1. Core Definition (1-2 sentences) – what it is and primary purpose
  2. Key Mechanisms (2-3 sentences) – how it works, main components, interactions
  3. Benefits & Advantages (2-3 sentences) – problems solved, improvements, impact
  4. Applications & Use Cases (1-2 sentences) – real-world examples
  5. Technical Details – metrics, performance, architecture, relationship properties
  6. Comparisons – differences from alternatives, relations to similar concepts
- Expand relationships fully: include property values, contextual links, chain connections
- Synthesize information into a coherent narrative instead of listing facts
- Connect insights from multiple tools into a complete understanding
- Ensure depth: cover at least 3-4 distinct aspects of the topic
- Minimum word count for simple queries: 100 words
- Target length for definition/purpose/mechanism queries: 150-250 words
- If the knowledge graph lacks required entities/relationships, state this explicitly, then answer using general or parametric knowledge

ANSWER QUALITY RULES
- Never give one-paragraph answers
- Never stop after a single tool call
- Include concrete examples, metrics, components wherever available
- Maintain logical narrative flow across paragraphs
- Fully integrate context from all retrieved data
- Plan tool usage strategically before synthesizing final answer
- Always provide a detailed, structured, multi-paragraph response

DELIVERABLE:
- Provide a clear, coherent, and detailed answer
- Reference specific relationships, entities, and properties from the knowledge graph
- State explicitly if knowledge graph data is missing, and provide general knowledge if necessary
- Answers must be at least 3-4 paragraphs with concrete, specific details
- Synthesize and connect facts instead of listing them

SIMPLIFICATION RULES:
- Replace jargon with everyday language
- Use analogies and real-world examples to explain complex concepts
- Break down technical terms into their basic meaning
- Explain acronyms and abbreviations on first use
- Convert complex mathematical concepts into intuitive descriptions
- Use concrete examples instead of abstract terminology
- Structure explanations from simple to complex
** Always use at least 2-3 tools to gather information from the KG before answering.
    Do not answer from your own knowledge unless the KG does not contain any relevant information.
    Provide multi-paragraph answers (3-4 paragraphs minimum) and include concrete details from the KG.
    Synthesize the information into a coherent narrative.**
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
                final_answer = final_message.content
                tool_calls = getattr(final_message, 'tool_calls', [])
                tool_call_count = len(tool_calls) if tool_calls else 0
            else:
                final_answer = "No answer generated"
                tool_call_count = 0
            
            print(f"\n💡 Final Answer:\n{final_answer}")
  
            print(f"\n{'='*90}\n")
            
            return {
                "question": question,
                "answer": final_answer,
                "success": True,
                "tool_calls": tool_call_count
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

    

    defaults = ("111", "111", "gemini", "gemini-2.5-flash")
    user_id="111"
    document_id="111"
    provider="gemini"
    model="gemini-2.5-flash"
    agent=Neo4jRAGSystem(user_id,document_id,provider,model)
     # Q&A Loop
    while True:
        q = input("\nQ: ").strip()
        if q.lower() in ['exit', 'quit']: break
        if not q: continue
        await agent.answer_question(q)

if __name__ == "__main__":
    asyncio.run(main())
