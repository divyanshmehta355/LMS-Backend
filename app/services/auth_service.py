from fastapi import HTTPException
from app.config import account

def register_user(email: str, password: str, userName: str):
    try:
        user = account.create("unique()", email=email, password=password, name=userName)
        return {"userId": user["$id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def send_otp(user_id: str, email: str):
    try:
        account.create_email_token(user_id=user_id, email=email)
        return {"message": "OTP sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def verify_otp(user_id: str, otp: str):
    try:
        session = account.create_session(user_id=user_id, secret=otp)
        return {"sessionToken": session["$id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def login_user(email: str, password: str):
    try:
        session = account.create_email_password_session(email=email, password=password)
        return {"sessionToken": session["$id"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def logout_user(session_id: str):
    try:
        account.delete_session(session_id=session_id)
        return {"message": "Logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
