from pydantic import BaseModel, Field

class Login(BaseModel):
    id : int
    email : str
    access_token : str
    refresh_token : str

class UserResponse(BaseModel):
    id : int
    email : str

class SignUp(BaseModel):
    user : UserResponse
    access_token : str
    refresh_token : str

class RefreshTokenRequest(BaseModel):
    refresh_token: str



