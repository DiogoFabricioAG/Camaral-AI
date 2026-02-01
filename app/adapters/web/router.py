from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.session_manager import manager

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        chat = manager.get_session(request.session_id)
        response = chat.send_message(request.message)
        return ChatResponse(response=response.text)
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e) + " in chat endpoint")
