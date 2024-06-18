from pydantic import BaseModel


class SignIn(BaseModel):
    email: str
    password: str


class SignUp(BaseModel):
    email: str
    password: str
    widgets: str


class Token(BaseModel):
    access_token: str
    token_type: str