### setup and activate the environment

```
python -m venv env
source env/bin/activate
```

### Install the required packages from requirements.txt

```
pip install -r requirements.txt
```

### Run commands

- **chunks retrieval**

```
python -m app.main
```

- **qa agent**

```
python -m src.qa_bot
```

### Environment Variables for LLM

| Provider           | Value              |
| ------------------ | ------------------ |
| GOOGLE_API_KEY     | your_api_key       |
| OPENAI_API_KEY     | your_api_key       |
| GROQ_API_KEY       | your_api_key       |
| HUGGING_FACE_AP    | your_api_key       |
| DEEPSEEK_API_KEY   | your_api_key       |
| MODEL_PROVIDER     | (ollama)           |
| EMBEDDING_PROVIDER | (ollama_embedding) |

### Changes made till now

```
src/
    model/
         config.py--(Model and Document retriever config)
         model_factory.py--(class for initializing LLM and Embedding model)

    document_retriever.py--(handles loading and chunking documents, and initialization of vector store through embedding factory)

    llm_manager.py--(initialization of LLM model. Model config is passed as argument to the model factory class to get the llm model.
    The class contains logic for retrieval chaining. It is a pipeline for retrieving similar chunks through query, and merging it with system prompt to generate the llm's response)

    qa_bot.py--(This is a final class for chat agent. Above classes will be initialized in this class as a property)

```
