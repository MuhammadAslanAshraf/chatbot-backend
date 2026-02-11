from app.services.tools.google_trends_mcp import fetch_google_trends
def detect_tool(message: str):
    msg = message.lower()

    if "trend" in msg or "popularity" in msg:
        return "trends"

    if "latest" in msg or "news" in msg or "search" in msg:
        return "tavily"

    return "normal"
async def handle_google_trends(message: str):
    # Extract keyword from message
    keyword = message.replace("trend", "").strip()
    data = await fetch_google_trends(keyword)
    return data