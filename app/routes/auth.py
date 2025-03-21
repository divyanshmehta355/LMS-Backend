from fastapi import APIRouter
from app.models.schemas import SignupRequest, OTPRequest, VerifyOTPRequest, LoginRequest, LogoutRequest
from app.services.auth_service import register_user, send_otp, verify_otp, login_user, logout_user

router = APIRouter()

@router.post("/signup")
def signup(request: SignupRequest):
    return register_user(request.email, request.password)

@router.post("/send-otp")
def send_otp_route(request: OTPRequest):
    return send_otp(request.userId, request.email)

@router.post("/verify-otp")
def verify_otp_route(request: VerifyOTPRequest):
    return verify_otp(request.userId, request.otp)

@router.post("/login")
def login(request: LoginRequest):
    return login_user(request.email, request.password)

@router.post("/logout")
def logout(request: LogoutRequest):
    return logout_user(request.sessionId)
