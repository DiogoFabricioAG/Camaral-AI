import os
from google import genai
from google.genai import types
from app.core.config import settings
from app.services.tools import CRMTools
from sqlalchemy.orm import Session

def get_system_instructions():
    path = os.path.join(os.getcwd(), "app", "INSTRUCTIONS.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def create_chat(db: Session):
    tools_instance = CRMTools(db)
    
    tool_list = [
        tools_instance.search_products,
        tools_instance.create_lead,
        tools_instance.create_payment
    ]
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=get_system_instructions(),
            tools=tool_list,
            temperature=0.7,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False
            )
        )
    )
    return chat
