import os

base_dir = r"d:\Multi-Agent Research Assistant\multi-agent-research-assistant"
dirs = [
    "backend/app/graph",
    "backend/app/tools",
    "backend/app/routes",
    "backend/tests",
    "frontend"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {
    "backend/app/__init__.py": "",
    "backend/app/models.py": "",
    "backend/app/graph/__init__.py": "",
    "backend/app/graph/state.py": "",
    "backend/app/graph/build_graph.py": "",
    "backend/app/tools/__init__.py": "",
    "backend/app/tools/web_search.py": "",
    "backend/app/routes/__init__.py": "",
    "backend/app/routes/research.py": "",
    "backend/tests/__init__.py": "",
    "backend/README.md": "# Backend\n",
    ".gitignore": ".env\n__pycache__/\n*.pyc\n.venv/\nvenv/\nnode_modules/\n",
    "backend/.env.example": "GROQ_API_KEY=your_groq_api_key_here\nOPENAI_API_KEY=your_openai_api_key_here\nTAVILY_API_KEY=your_tavily_api_key_here\nMAX_RESEARCH_LOOPS=2\n",
    "backend/app/config.py": '''from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    tavily_api_key: str
    max_research_loops: int = 2

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
''',
    "backend/app/main.py": '''from fastapi import FastAPI
from app.config import settings

app = FastAPI(title="Multi-Agent Research Assistant")

@app.get("/health")
def health_check():
    return {"status": "ok"}
''',
    "backend/app/graph/nodes.py": '''def planner_node(state):
    """
    Takes the original question and breaks it down into specific, 
    researchable sub-questions.
    """
    pass

def researcher_node(state):
    """
    Calls the Tavily search tool for the current sub-question and 
    appends the results to the research results.
    """
    pass

def analyzer_node(state):
    """
    Analyzes gathered research to extract key findings and determines 
    if more research is needed to answer all sub-questions.
    """
    pass

def writer_node(state):
    """
    Synthesizes a structured markdown report from the findings and 
    the original question.
    """
    pass
''',
    "backend/pyproject.toml": '''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "multi-agent-research-assistant"
version = "0.1.0"
description = "Multi-Agent Research Assistant Backend"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "fastapi",
    "uvicorn",
    "pydantic-settings",
    "langgraph",
    "langchain",
    "langchain-groq",
    "langchain-openai",
    "tavily-python"
]
'''
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Scaffolding complete.")
