from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.chat_service import handle_chat
import asyncio

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: str | None = None

@router.post("/chat")
async def chat(request: ChatRequest):

    response_text = await handle_chat(
        request.user_id,
        request.message,
        request.conversation_id
    )

    async def stream():
        for word in response_text.split():
            yield word + " "
            await asyncio.sleep(0.05)

    return StreamingResponse(stream(), media_type="text/plain")
