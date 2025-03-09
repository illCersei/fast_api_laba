from pydantic import BaseModel, Field

class Login(BaseModel):
    access_token : str

class UserResponse(BaseModel):
    id : int
    login : str

class SignUp(BaseModel):
    user : UserResponse
    access_token : str

