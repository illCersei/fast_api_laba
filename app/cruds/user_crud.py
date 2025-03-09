from sqlalchemy.orm import Session
from app.models.users import Users
from app.schemas.user_schema import UserCreate, UserLogin
from app.auth.auth_handler import sign_jwt

def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def creating_user(db: Session, user: UserCreate):
    new_user = Users(login=user.login, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = sign_jwt(new_user.login)

    return {"user": {"id": new_user.id, "login": new_user.login}, "access_token": token}


def loggining_user(db: Session, user: UserLogin):
    return sign_jwt(user.login)
