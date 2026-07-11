from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from app.config import settings
import os

def get_chat_model():
    if settings.groq_api_key:
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=settings.groq_api_key
        )
    elif settings.openai_api_key:
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=settings.openai_api_key
        )
    else:
        raise RuntimeError(
            "No LLM configured. Please set GROQ_API_KEY or OPENAI_API_KEY in the environment."
        )
