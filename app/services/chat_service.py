import uuid
import asyncio
from fastapi.concurrency import run_in_threadpool
from app.services.db.supabase_client import supabase
from app.services.tool_router import detect_tool
from app.services.tools import tavily, google_trends_mcp
from app.services.memory_service import update_memory
from app.services.tools.google_trends_mcp import fetch_google_trends

async def handle_google_trends(message: str):
    # Extract keyword from message
    keyword = message.replace("trend", "").strip()
    data = await fetch_google_trends(keyword)
    return data

async def handle_chat(user_id: str, message: str, conversation_id: str | None):

    # Ensure user
    await run_in_threadpool(
        lambda: supabase.table("users")
        .upsert({"id": user_id})
        .execute()
    )

    # Conversation
    conversation_id = conversation_id or str(uuid.uuid4())

    await run_in_threadpool(
        lambda: supabase.table("conversations")
        .upsert({
            "id": conversation_id,
            "user_id": user_id
        }).execute()
    )

    # Store user message
    await run_in_threadpool(
        lambda: supabase.table("messages")
        .insert({
            "conversation_id": conversation_id,
            "role": "user",
            "content": message
        }).execute()
    )

    # Detect tool
    tool = detect_tool(message)

    if tool == "tavily":
        tool_result = await tavily.fetch_tavily(message)
        results = tool_result.get("results", [])[:3]

        formatted = "Here are the latest updates:\n\n"

        for idx, item in enumerate(results, 1):
            formatted += f"{idx}. {item['title']}\n"
            formatted += f"   {item['content'][:150]}...\n"
            formatted += f"   Source: {item['url']}\n\n"

        response_text = formatted

    elif tool == "trends":
        tool_result = await google_trends_mcp.fetch_google_trends(message)
        response_text = str(tool_result)

    else:
        response_text = "No tool matched your request."

    # Store assistant message
    await run_in_threadpool(
        lambda: supabase.table("messages")
        .insert({
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": response_text,
            "tool_used": tool
        }).execute()
    )

    # Update memory
    await update_memory(user_id, f"User asked: {message}")

    return response_text
  
  

