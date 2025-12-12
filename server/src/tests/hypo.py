template = """
You are on an important mission to generate a narrative summary of the provided paper. Your task is to create a concise and informative summary that captures the essence of the paper, including its key findings, methodologies, and conclusions.

Your summary should be structured in a way that is easy to understand and provides a clear overview of the paper's contributions to its field. Focus on the most significant aspects of the research, avoiding unnecessary details or jargon.

If you encounter any difficult or complex concepts, explain them in simple terms to ensure clarity for a broad audience.

Your summary should be no more than {length} characters long, and it should be written in a narrative style that flows logically from one point to the next without abrupt transitions or special headings or formatting. The summary should be written in a way that is engaging and informative, suitable for readers who may not be experts in the field.

Write the summary in plain text, with minimal syntax formatting for citations.

Include any citations or references to specific sections of the paper, reproducing the raw text. It should read like a cohesive brief that could be read on a podcast or in a blog post.

Citations should be formatted as [^1], [^2], etc., where each number corresponds to the idx of the list of citations you will provide at the end of the summary.

Here is the pdf text which you would use to generate a summary
{text}

"""
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.6,
    top_p=0.95,
)


prompt = PromptTemplate(
    input_variables=["text","length"],
    template=template
)

chain = prompt | llm
while True:
 query=input("Q: ")
 response=chain.invoke({"text":query,"length":"15000"})
 print(response.content)
