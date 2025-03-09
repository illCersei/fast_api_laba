import time
import jwt
from typing import Dict
from app.core.config import settings  

def token_response(access_token: str, refresh_token : str) -> Dict[str, str]:
    return {"access_token": access_token,
            "refresh_token": refresh_token}

def sign_jwt(login: str) -> Dict[str, str]:
    access_payload = {
        "login": login,
        "expires": time.time() + settings.ACCESS_TOKEN_EXPIRE_SECONDS
    }
    refresh_payload = {
        "login": login,
        "expires": time.time() + settings.REFRESH_TOKEN_EXPIRE_SECONDS
    }

    access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    token_response(access_token, refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token} 

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
def verify_refresh_token(refresh_token: str) -> str | None:
    payload = decode_jwt(refresh_token)
    if payload:
        return payload["login"]
    return None