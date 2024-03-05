from peewee import MySQLDatabase
from app.config import DB_USER, DB_PASSWORD, DB_DATABASE, DB_HOST

db = MySQLDatabase(DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

from .user import User, SignupRequest, LoginRequest, UserDetail
from .auth import Token, TokenData
from .task import Task, TaskDetail, TaskFullDetail, TaskCreate, LocationInfo
