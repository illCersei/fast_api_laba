from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.cruds.user_crud import creating_user, loggining_user
from app.schemas.user_schema import UserCreate, UserLogin
from fastapi.responses import FileResponse
from app.auth.auth_bearer import JWTBearer

from app.schemas.auth import Login



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sign-up", response_model=dict) #response na pydantic smenit'
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return creating_user(db, user)

@router.get("/test", dependencies=[Depends(JWTBearer())])
async def test():
    return FileResponse("app/static/index.html")

@router.get("/test2")
async def test2():
    return FileResponse("app/static/index.html")

@router.post("/login", response_model=Login) 
def login_user(user : UserLogin, db : Session = Depends(get_db)):
    return loggining_user(db, user)