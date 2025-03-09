from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "login": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }