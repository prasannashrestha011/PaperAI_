import requests
from database.supabase_client import supabase 
from io import BytesIO
from unstructured.partition.pdf import partition_pdf
# Download PDF bytes
url="https://cwlklruqhmtcgrtsrmkh.supabase.co/storage/v1/object/public/pdfs/1cfeba82-12ac-4bdd-b77c-c26973fd5551/e6408819-88cb-4a11-8f85-b45452bb1ae5/Energy_Storage_Scheduling_for_Cost_Minimization_Using_Deep_Q-Learning.pdf"
response = requests.get(url)
pdf_bytes = response.content

# Wrap bytes in BytesIO
pdf_file_like = BytesIO(pdf_bytes)

# Extract text
elements = partition_pdf(file=pdf_file_like, strategy="fast", infer_table_structure=False)
text_content = "".join(str(el) for el in elements)

print(text_content)
