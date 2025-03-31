from sqlalchemy.orm import Session
from app.models.users import Users
from app.schemas.user_schema import UserCreate, UserLogin
from app.auth.auth_handler import sign_jwt, verify_refresh_token, decode_jwt
from fastapi.exceptions import HTTPException
from app.auth.security import hash_password, verify_password
from app.schemas.auth import RefreshTokenRequest
from app.core.config import settings

def creating_user(db: Session, user: UserCreate):
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    hashed_pass = hash_password(user.password)
    new_user = Users(email=user.email, password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    tokens = sign_jwt(new_user.email)

    return {
        "user": {"id": new_user.id, "email": new_user.email},
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"]
    }

def loggining_user(db: Session, user: UserLogin):
    existing_user = db.query(Users).filter(Users.email == user.email).first()

    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Ошибка входа")

    return sign_jwt(existing_user.id ,user.email)

def refreshing_users_token(request: RefreshTokenRequest):
    email = verify_refresh_token(request.refresh_token)
    if not email:
        raise HTTPException(status_code=403, detail="Invalid or expired refresh token")
    
    return sign_jwt(email)

def get_users_info(db: Session, token : str) -> dict :

    payload = decode_jwt(token)

    query = db.query(Users.id, Users.email).filter(Users.email==payload["email"]).first()
    return {"id": query.id, "email": query.email}
