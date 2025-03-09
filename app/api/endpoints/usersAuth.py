from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.cruds.user_crud import creating_user, loggining_user
from app.schemas.user_schema import UserCreate, UserLogin
from fastapi.responses import FileResponse
from app.auth.auth_bearer import JWTBearer

from app.schemas.auth import Login, RefreshTokenRequest, SignUp

from app.auth.auth_handler import decode_jwt, verify_refresh_token, sign_jwt

from datetime import datetime, timezone


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sign-up", response_model=SignUp) #response na pydantic smenit'
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return creating_user(db, user)

@router.post("/login", response_model=Login) 
def login_user(user : UserLogin, db : Session = Depends(get_db)):
    return loggining_user(db, user)

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    login = verify_refresh_token(request.refresh_token)
    if not login:
        raise HTTPException(status_code=403, detail="Invalid or expired refresh token")
    
    return sign_jwt(login)








@router.get("/test/info", dependencies=[Depends(JWTBearer())]) #protected
def test(token : str = Depends(JWTBearer())):

    payload = decode_jwt(token)
    cringe_time = payload.get("expires")
    current_time = datetime.now(timezone.utc).timestamp()
    token_left = cringe_time - current_time

    return {
        "tokeny_ostalos" : token_left
    }

@router.get("/test", dependencies=[Depends(JWTBearer())])
def test_file():
    return FileResponse("app/static/index.html")


@router.get("/test2")
def test2():
    return FileResponse("app/static/index.html")

