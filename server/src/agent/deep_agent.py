import asyncio
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader

def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)

load_dotenv()

# --- Configure for maximum output ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.6,
    top_p=0.95,
)

# --- Multi-stage prompt with selective citation strategy ---
template = """You are a detailed research analyst. Analyze the PDF and provide an in-depth answer.
PDF CONTENT:
{pdf_text}

QUESTION: {query}
You are in detailed mode. Provide a comprehensive and thorough answer to the user's question. Include relevant details, explanations, and context to ensure clarity and understanding.

You are an excellent researcher who provides precise, evidence-based answers from academic papers. Your responses must always include specific text evidence from the paper. You give holistic answers, not just snippets. Help the user understand the paper's content and context. Your answers should be clear, concise, and informative.

Follow these strict formatting rules:
1. Structure your answer in two parts:
   - **Main response** with numbered citations [^1], [^6, ^7], etc., where each number corresponds to a specific piece of evidence.
   - **Evidence** section with strict formatting

2. If the main response requires mathematical notation, use LaTeX syntax, surrounded by triple backticks in a `math` context. For example, use "```math" to denote the start and end of the equation block. Like this:
   ```math
   \\frac{{a}}{{b}} &= c \\\\
   \\frac{{d}}{{e}} &= f
   ```

Display Math notation, even in LaTeX syntax, MUST be in a math code block.

Inline Math notation should be wrapped in double dollar signs, like this: $$\\frac{{a}}{{b}} = c$$ or this: $$d_v$$.

3. Format the evidence section as follows:
   ---EVIDENCE---
   @cite[1]
   "First piece of evidence"
   @cite[2]
   "Second piece of evidence"
   ---END-EVIDENCE---

4. Each citation must:
   - Start with @cite[n] on its own line
   - Have the quoted text on the next line
   - Have a unique citation number `n` for each piece of evidence
   - Include only relevant quotes that directly support your claims
   - Be in plaintext

5. If you're not sure about the answer, let the user know you're uncertain. Provide your best guess, but do not fabricate information.

6. Citations should always be numbered sequentially, starting from 1.

7. If your response is re-using an existing citation, create a new one with the same text for this evidence block.

8. If the paper is not relevant to the question, say so and provide a brief explanation.

9. If the user is asking for data, metadata, or a comparison, provide a table with the relevant information in Markdown format.

10. ONLY use citations if you're including evidence from the paper. Do not use citations if you are not including evidence.

11. You are not allowed any html formatting. Only use Markdown, LaTeX, and code blocks.


Example format:

The study found that machine learning models can effectively detect spam emails [^1]. However, their performance decreases when dealing with sophisticated phishing attempts [^2].

---EVIDENCE---
@cite[1]
"Our experiments demonstrated 98% accuracy in spam detection using the proposed neural network architecture"
@cite[2]
"The false negative rate increased to 23% when testing against advanced social engineering attacks"
---END-EVIDENCE---
"""

prompt = PromptTemplate(
    input_variables=["pdf_text", "query"],
    template=template
)

chain = prompt | llm

async def answer_question(query: str, text: str):
    for chunk in chain.stream({
        "pdf_text": text,
        "query": query
    }):
        content = chunk.content
        if isinstance(content, (list, dict)):
            content = str(content)
        yield content 
        await asyncio.sleep(0)

