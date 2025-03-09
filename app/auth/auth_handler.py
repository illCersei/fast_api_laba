import time
import jwt
from typing import Dict
from app.core.config import settings  

def token_response(token: str) -> Dict[str, str]:
    return {"access_token": token}

def sign_jwt(login: str) -> Dict[str, str]:
    payload = {
        "login": login,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token_response(token)

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}