from pydantic import BaseModel, EmailStr

class ChatRequest(BaseModel):
    message: str

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
