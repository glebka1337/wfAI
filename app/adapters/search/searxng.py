import aiohttp
import logging
from typing import List, Dict
from app.domain.interfaces.tools.search import ISearchTool

logger = logging.getLogger(__name__)

class SearXNGSearchTool(ISearchTool):
    def __init__(self, base_url: str = "http://searxng:8080"):
        self.base_url = base_url.rstrip("/")
        
    async def search(self, query: str) -> str:
        """
        Queries the local SearXNG instance and returns a formatted summary.
        """
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "q": query,
                    "format": "json",
                    "language": "auto"
                }
                async with session.get(f"{self.base_url}/search", params=params) as resp:
                    if resp.status != 200:
                        logger.error(f"SearXNG returned status {resp.status}")
                        return "Error: Unable to perform search."
                    
                    data = await resp.json()
                    results = data.get("results", [])
                    
                    if not results:
                        return "No results found."
                    
                    # Format top 3 results
                    formatted = []
                    for idx, res in enumerate(results[:3], 1):
                        title = res.get("title", "No Title")
                        content = res.get("content", "No Content")
                        url = res.get("url", "#")
                        formatted.append(f"{idx}. {title}: {content} ({url})")
                        
                    return "\n".join(formatted)
                    
        except Exception as e:
            logger.exception("Search tool error")
            return f"Error performing search: {str(e)}"
