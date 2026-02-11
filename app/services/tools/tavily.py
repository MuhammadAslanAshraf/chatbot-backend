import httpx
from app.core.config import TAVILY_API_KEY

async def fetch_tavily(query: str):
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    payload = {"query": query}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.tavily.com/search", headers=headers, json=payload)
        return response.json()
