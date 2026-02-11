from fastapi.concurrency import run_in_threadpool
from app.services.db.supabase_client import supabase
async def update_memory(user_id: str, summary: str):
    await run_in_threadpool(
        lambda: supabase.table("memory_context")
        .upsert({
            "user_id": user_id,
            "summary": summary
        })
        .execute()
    )
