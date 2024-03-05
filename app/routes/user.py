from fastapi import APIRouter, Depends

from app.dependencies.authentication import get_current_user
from app.models import UserDetail, User

user_router = APIRouter()


@user_router.get("/user", tags=['User'])
async def get_user(user: User = Depends(get_current_user)) -> UserDetail:
    """
       Retrieve user details based on the provided user object and return the user detail.
    """
    user_detail = UserDetail(**user.to_dict())
    return user_detail
