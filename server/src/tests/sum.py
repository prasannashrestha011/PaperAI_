
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

template = """
Generate a structured research summary of the provided paper in approximately {length} characters.

Format the summary with these clear sections (use these exact section headers):

**Paper Title** (if available, otherwise skip)

**Opening paragraph**: A concise statement of what the paper presents - its main contribution and scope.

**Motivation**: Explain the problem context, why this research is needed, what gaps or challenges exist in current approaches, and the driving factors behind this work. Support claims with citations.

**Methodology**: Describe the proposed approach, framework, or system architecture. Break down key components, techniques, or modules. Explain how the approach works and what makes it novel or different. Use clear subsections if multiple components exist.

**Key Findings**: Present the main results, discoveries, or identified challenges. Include specific metrics, comparisons, performance numbers, or important observations. Support with citations.

**Implications and Applications**: Conclude with the significance of this work - what domains benefit, what practical applications exist, what future directions are proposed, and why this research matters.

Style requirements:
- Use bold for section headers: **Motivation**, **Methodology**, etc.
- Write in clear, academic paragraphs within each section
- Use direct, factual statements - avoid phrases like "imagine a world" or rhetorical questions
- Include inline citations [^X] to support specific claims
- Maintain professional, objective tone throughout
- Each section should flow logically into the next
- No bullet points in the main narrative (only use if listing technical components)

Paper text:
{text}

Generate the summary now:
"""

prompt = PromptTemplate(
    input_variables=["pdf_text", "query"],
    template=template
)

chain = prompt | llm

text = extract_pdf_text("../data/sample.pdf")

print("Generating comprehensive response...\n")
full_response = ""

for chunk in chain.stream({
    "text": text,
    "length":"8000"
}):
    content = chunk.content
    print(content, end="", flush=True)
    full_response += content

print(f"\n\n--- Total Length: {len(full_response)} characters ---")
print(f"--- Word Count: {len(full_response.split())} words ---")
