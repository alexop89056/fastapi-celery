import re

from bcrypt import hashpw, gensalt
from fastapi.exceptions import HTTPException
from peewee import Model, CharField
from pydantic import BaseModel, validator, Field

from app.models import db


class User(Model):
    """
        User database model
    """
    username = CharField(unique=True)
    # email = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    fullname = CharField()

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname
        }

    class Meta:
        database = db


class SignupRequest(BaseModel):
    """
        Signup request Pydantic base model
    """
    username: str = Field(..., example="admin")
    password: str = Field(..., example="TGAnv1hu0N")
    email: str = Field(..., example="JtJy6@example.com")
    fullname: str = Field(..., example="admin admin")

    @validator("username")
    def unique_username(cls, value):
        if not value.strip():
            raise HTTPException(status_code=400, detail="Username cannot be blank")

        try:
            user = User.get(User.username == value)
            raise HTTPException(status_code=400, detail="USer with this username already exists")
        except User.DoesNotExist:
            return value

    @validator("password")
    def password_hash(cls, value):
        if not value.strip():
            raise HTTPException(status_code=400, detail="Username cannot be blank")
        hashed_password = hashpw(value.encode('utf-8'), gensalt())
        return hashed_password

    @validator("email")
    def unique_email(cls, value):

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(email_regex, value)
        if not bool(match):
            raise HTTPException(status_code=400, detail="Invalid email address")

        if not value.strip():
            raise HTTPException(status_code=400, detail="Email cannot be blank")

        try:
            user = User.get(User.email == value)
            raise HTTPException(status_code=400, detail="User with this email already exists")
        except User.DoesNotExist:
            return value

    @validator("fullname")
    def validate_fullname(cls, value):
        if not value.strip():
            raise HTTPException(status_code=400, detail="Fullname cannot be blank")
        return value


class LoginRequest(BaseModel):
    """
        Login request Pydantic base model
    """
    username: str = Field(..., example="admin")
    password: str = Field(..., example="TGAnv1hu0N")

    @validator("username")
    def unique_username(cls, value):
        if not value.strip():
            raise HTTPException(status_code=400, detail="Username cannot be blank")

        try:
            user = User.get(User.username == value)
            return value
        except User.DoesNotExist:
            raise HTTPException(status_code=400, detail="Username not found")


class UserDetail(BaseModel):
    """
        User detail Pydantic base model
    """
    username: str
    email: str
    fullname: str
