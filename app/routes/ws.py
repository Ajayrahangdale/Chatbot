from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    token = websocket.query_params.get("token")
    
    if not token:
        print("❌ Token missing in WebSocket request.")
        await websocket.close(code=1008)
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        if not user:
            print("❌ User not found in token payload.")
            await websocket.close(code=1008)
            return
    except JWTError as e:
        print(f"❌ JWT decode error: {e}")
        await websocket.close(code=1008)
        return

    await websocket.accept()
    print(f"✅ WebSocket connected for user: {user}")
    await websocket.send_text(f"🧠 Hello {user}! Welcome to ZenifyAI Chat.")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Message from {user}: {data}")
            await websocket.send_text(f"ZenifyAI: You said - {data}")
    except WebSocketDisconnect:
        print(f"🔌 WebSocket disconnected for user: {user}")
