from typing import Dict, List
from uuid import uuid4
from fastapi import Request, Response

# In-memory storage for session data
session_storage: Dict[str, List[Dict[str, str]]] = {}

# Function to generate unique session IDs
def generate_session_id() -> str:
    return str(uuid4())

# Middleware for session management
async def add_session_id_to_request(request: Request, call_next):
    # Check if session ID exists in cookies
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        # Generate a new session ID if it doesn't exist
        session_id = generate_session_id()
        session_storage[session_id] = []

    request.state.session_id = session_id
    
    response: Response = await call_next(request)
    
    # Set the session ID cookie in the response
    response.set_cookie(key="session_id", value=session_id)
    
    return response

# Function to retrieve conversation context
def get_conversation_context(session_id: str) -> List[Dict[str, str]]:
    session_data = session_storage.get(session_id, {})
    return session_data.get("context", [])