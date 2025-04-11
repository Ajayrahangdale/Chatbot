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
        await websocket.close(code=1008)
        return
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        if not user:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    await websocket.send_text(f"🧠 Hello {user}! Welcome to ZenifyAI Chat.")
    try:
        while True:
            data = await websocket.receive_text()
            # For now, echo back the message. Replace with actual AI call later.
            await websocket.send_text(f"ZenifyAI: You said - {data}")
    except WebSocketDisconnect:
        print("🔌 WebSocket disconnected")
