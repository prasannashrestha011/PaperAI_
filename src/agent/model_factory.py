"""
This module handles loading chat and embedding model from different providers 

Chat models-> Gemini, OpenAI, DeepSeek ,Groq
Embedding models-> 
  local: 
    - HuggingFace(sentence-transformers/all-MiniLM-L6-v2)
  cloud:
    - OpenAI, Gemini(embedding-001)
"""

"""Chat model packages"""
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

"""Embeddings packages"""
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import OllamaEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()


class ModelFactory:

    @staticmethod
    def create_chat_model(provider: str, model_name: str, temperature: float):
        if provider == "gemini":
            return ModelFactory._create_gemini_model(model_name, temperature)
        elif provider == "openai":
            return ModelFactory._create_openai_model(model_name, temperature)
        elif provider == "deepseek":
            return ModelFactory._create_deepseek_model(model_name, temperature)
        elif provider == "ollama":
            return ModelFactory._create_ollama_model(model_name, temperature)
        elif provider=="groq":
            return 
        else:
            raise ValueError(f"Unsupported model provider: {provider}")

    @staticmethod
    def _create_openai_model(model_name: str, temperature: float):
        return ChatOpenAI(model=model_name, temperature=temperature)

    @staticmethod
    def _create_gemini_model(model_name: str, temperature: float):
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            
        )

    @staticmethod
    def _create_deepseek_model(model_name: str, temperature: float):
        return ChatDeepSeek(model=model_name, temperature=temperature)

    @staticmethod
    def _create_ollama_model(model_name: str, temperature: float):
        return ChatOllama(model=model_name, temperature=temperature)
    
    @staticmethod
    def _create_groq_model(model_name:str,temperature:float):
        return ChatGroq(model=model_name,temperature=temperature)



class Embedding_Factory:
    @staticmethod
    def create_embedding(
        provider: str, model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        if provider == "hugging-face":
            embedding = HuggingFaceEmbeddings(model_name=model)
        if provider == "openai":
            embedding = OpenAIEmbeddings(model=model)
        if provider == "gemini":
            embedding = GoogleGenerativeAIEmbeddings(model=model)
        if provider == "ollama":
            embedding = OllamaEmbeddings(model=model)
        return embedding
