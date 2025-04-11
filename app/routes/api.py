from fastapi import APIRouter, Depends, HTTPException
from app import schemas, utils
from app.mongodb import db
from openai import OpenAI
from dotenv import load_dotenv
import os
from app.utils import get_current_user

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
router = APIRouter()

# ✅ Home route
@router.get("/")
def root():
    return {"message": "ZenifyAI backend working perfectly ✅"}

# ✅ Chat
@router.post("/chat")
async def chat_endpoint(request: schemas.ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ZenifyAI, a helpful and kind mental health assistant."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# ✅ Register
@router.post("/register")
async def register_user(user: schemas.UserSchema):
    user_exist = await db.users.find_one({"email": user.email})
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = utils.hash_password(user.password)
    user_dict = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_pwd
    }

    result = await db.users.insert_one(user_dict)
    return {"id": str(result.inserted_id), "email": user.email, "name": user.name}

# ✅ Login
@router.post("/login")
async def login_user(user: schemas.UserLogin):
    user_data = await db.users.find_one({"email": user.email})
    if not user_data or not utils.verify_password(user.password, user_data["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = utils.create_access_token({"sub": user_data["email"]})
    return {"access_token": token, "token_type": "bearer"}

# ✅ Profile
@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {current_user['sub']}!"}


# app/routes/api.py

@router.post("/chat")
async def chat_endpoint(request: schemas.ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ZenifyAI, a helpful and kind mental health assistant."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
