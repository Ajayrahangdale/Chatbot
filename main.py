# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()
            print(f"User: {user_message}")

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly mental health assistant."},
                    {"role": "user", "content": user_message},
                ],
            )

            bot_reply = response.choices[0].message.content.strip()
            await websocket.send_text(bot_reply)

    except WebSocketDisconnect:
        print("Client disconnected")
