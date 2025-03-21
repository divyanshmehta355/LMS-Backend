from pydantic import BaseModel

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
