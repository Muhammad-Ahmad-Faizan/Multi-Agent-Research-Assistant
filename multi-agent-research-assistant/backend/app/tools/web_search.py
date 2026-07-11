from tavily import AsyncTavilyClient
from app.config import settings
from typing import List, Dict
import asyncio
import logging

logger = logging.getLogger(__name__)

async def search_web(query: str, timeout: int = 15) -> List[Dict]:
    """
    Search the web using Tavily asynchronously.
    Returns a list of dicts with {source_url, title, snippet}
    """
    if not settings.tavily_api_key:
        raise RuntimeError("TAVILY_API_KEY is not configured.")
        
    client = AsyncTavilyClient(api_key=settings.tavily_api_key)
    
    try:
        # Wrap with asyncio.wait_for to enforce a strict timeout
        response = await asyncio.wait_for(
            client.search(query=query, max_results=3),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        logger.error(f"Tavily search timeout out after {timeout} seconds for query: {query}")
        return []
    except Exception as e:
        logger.error(f"Tavily search failed for query: {query}. Error: {str(e)}")
        return []
        
    results = []
    for r in response.get("results", []):
        content = r.get("content", "")
        if len(content) > 400:
            content = content[:400] + "..."
            
        results.append({
            "source_url": r.get("url"),
            "title": r.get("title"),
            "snippet": content
        })
    return results
