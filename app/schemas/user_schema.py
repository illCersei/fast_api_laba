from pydantic import BaseModel

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    login: str
    password: str

