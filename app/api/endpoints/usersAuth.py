from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.cruds.user_crud import creating_user, loggining_user
from app.schemas.user_schema import UserCreate, UserLogin
from fastapi.responses import FileResponse
from app.models.auth import UserLoginSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sign-up", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return creating_user(db, user)

@router.get("/test")
def test():
    return FileResponse("index.html")

@router.post("/login", response_model=dict) 
def login_user(user : UserLogin, db : Session = Depends(get_db)):
    return loggining_user(db, user)