from pydantic import BaseModel, Field

class Login(BaseModel):
    id : int
    email : str
    access_token : str
    refresh_token : str

class SignUp(BaseModel):
    id : int
    email : str
    access_token : str
    refresh_token : str

class RefreshTokenRequest(BaseModel):
    refresh_token: str



