from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from appwrite.client import Client
from appwrite.services.account import Account
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Client()
client.set_endpoint(os.getenv("APPWRITE_ENDPOINT"))
client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
client.set_key(os.getenv("APPWRITE_API_KEY"))

account = Account(client)

class SignupRequest(BaseModel):
    email: str
    password: str

class OTPRequest(BaseModel):
    userId: str
    email: str

class VerifyOTPRequest(BaseModel):
    userId: str
    otp: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    sessionId: str

@app.post("/signup")
def signup(request: SignupRequest):
    try:
        user = account.create("unique()", email=request.email, password=request.password)
        return {"userId": user["$id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send-otp")
def send_otp(request: OTPRequest):
    try:
        result = account.create_email_token(user_id=request.userId, email=request.email)
        return {"message": "OTP sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest):
    try:
        session = account.create_session(user_id=request.userId, secret=request.otp)
        return {"sessionToken": session["$id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/login")
def login(request: LoginRequest):
    try:
        session = account.create_email_password_session(email=request.email, password=request.password)
        return {"sessionToken": session["$id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/logout")
def logout(request: LogoutRequest):
    try:
        account.delete_session(session_id=request.sessionId)
        # account.delete_session('current') // To delete the curr user.
        return {"message": "Logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)