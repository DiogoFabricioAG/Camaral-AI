from app.services.gemini_service import create_chat
from app.adapters.db import SessionLocal

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id: str):
        if session_id not in self.sessions:
            db = SessionLocal() 
            self.sessions[session_id] = create_chat(db)
        return self.sessions[session_id]

    def close_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

manager = SessionManager()
