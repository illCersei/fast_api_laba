from sqlalchemy.orm import Session
from app.models.users import Users
from app.schemas.user_schema import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    new_user = Users(login=user.login, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
