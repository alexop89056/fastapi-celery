import re
from typing import Optional

from fastapi import HTTPException
from peewee import Model, CharField, BooleanField
from pydantic import BaseModel, validator, Field

from app.models import db


class Task(Model):
    """
        Task database model
    """
    ip = CharField()
    completed = BooleanField(default=False)
    is_eu = BooleanField(null=True)
    city = CharField(null=True)
    region = CharField(null=True)
    country_name = CharField(null=True)
    latitude = CharField(null=True)
    longitude = CharField(null=True)
    calling_code = CharField(null=True)

    def __str__(self):
        return f"<Task: {self.id}>"

    def to_dict(self):
        return {
            'ip': self.ip,
            'completed': self.completed or False,
            'is_eu': self.is_eu or False,
            'city': self.city or 'N/A',
            'region': self.region or 'N/A',
            'country_name': self.country_name or 'N/A',
            'latitude': self.latitude or 'N/A',
            'longitude': self.longitude or 'N/A',
            'calling_code': self.calling_code or 'N/A'
        }

    class Meta:
        database = db


class TaskCreate(BaseModel):
    """
        Task create Pydantic base model
    """
    ip: str = Field(..., example="8.8.8.8")

    @validator("ip")
    def validate_ip(cls, value):
        if not value.strip():
            raise HTTPException(status_code=400, detail="IP cannot be blank")

        ipv4_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        if not ipv4_pattern.match(value):
            raise HTTPException(status_code=400, detail="IP cannot be blank")

        return value


class TaskDetail(BaseModel):
    """
        Task detail Pydantic base model
    """
    id: int


class TaskFullDetail(BaseModel):
    """
        Task full detail Pydantic base model
    """
    ip: str = Field(..., example="8.8.8.8")
    completed: bool = Field(..., example=False)
    is_eu: bool = Field(..., example=False)
    city: str = Field(..., example="Moscow")
    region: str = Field(..., example="Moscow")
    country_name: str = Field(..., example="Russia")
    latitude: str = Field(..., example="55.751244")
    longitude: str = Field(..., example="37.618423")
    calling_code: str = Field(..., example="+7")


class LocationInfo(BaseModel):
    """
        Location info Pydantic base model
    """
    is_eu: Optional[bool]
    city: Optional[str]
    region: Optional[str]
    country_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    calling_code: Optional[str]
