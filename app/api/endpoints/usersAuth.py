from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.cruds.user_crud import create_user
from app.schemas.user_schema import UserCreate
from fastapi.responses import FileResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sign-up", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/test")
def test():
    return FileResponse("index.html")
