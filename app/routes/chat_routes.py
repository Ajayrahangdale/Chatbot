from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from starlette.websockets import WebSocketState
from jose import jwt, JWTError

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"

router = APIRouter()

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token")
        return user_id
    except JWTError:
        raise ValueError("Token verification failed")

def generate_bot_reply(user_message: str) -> str:
    user_message = user_message.lower()
    if "sad" in user_message or "depressed" in user_message:
        return "I'm here for you. You are not alone. 💜"
    elif "happy" in user_message:
        return "That's wonderful! Keep smiling 😊"
    elif "stress" in user_message:
        return "Try taking deep breaths. Want a short meditation session?"
    else:
        return "I hear you. Let's talk more about how you're feeling."

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    try:
        user_id = verify_token(token)
        await websocket.accept()
        print(f"✅ WebSocket Connected: {user_id}")
        await websocket.send_text("✅ Connected to ZenifyAI")

        while True:
            if websocket.application_state != WebSocketState.CONNECTED:
                break

            data = await websocket.receive_text()
            reply = generate_bot_reply(data)
            await websocket.send_text(reply)

    except WebSocketDisconnect:
        print("❌ Client Disconnected")
    except Exception as e:
        print(f"❌ WebSocket Error: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
