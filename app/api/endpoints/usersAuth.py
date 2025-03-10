from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.cruds.user_crud import creating_user, loggining_user, refreshing_users_token, get_users_info
from app.schemas.user_schema import UserCreate, UserLogin
from fastapi.responses import FileResponse
from app.auth.auth_bearer import JWTBearer

from app.schemas.auth import Login, RefreshTokenRequest, SignUp

from app.auth.auth_handler import decode_jwt

from datetime import datetime, timezone

from app.services.binary import ImageBase64Request, decode_base64_to_image, bradley_threshold, encode_image_to_base64


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
    return refreshing_users_token(request)

@router.get("/users/me", dependencies=[Depends(JWTBearer())])
def info_user(token : str = Depends(JWTBearer())):
    return get_users_info(token)

@router.post("/binary_image")
def process_binary_image(request: ImageBase64Request):
    """ Принимает изображение в base64, бинаризует его и возвращает обратно в base64 """
    image = decode_base64_to_image(request.image_base64)  # Декодируем base64 в NumPy
    binary_image = bradley_threshold(image)  # Бинаризуем изображение
    binary_base64 = encode_image_to_base64(binary_image)  # Кодируем обратно в base64
    return {"binary_image_base64": binary_base64}  # Возвращаем результат


@router.get("/test/info", dependencies=[Depends(JWTBearer())]) #protected
def test(token : str = Depends(JWTBearer())):

    payload = decode_jwt(token)
    print(payload)
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

