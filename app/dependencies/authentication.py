from fastapi import Depends, HTTPException

from app.auth.jwt import decode_jwt_token, oauth2_scheme
from app.models import User


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
        Get the current user using the provided token.
        Parameters:
            token (str): The authentication token.
        Returns:
            User: The current user.
    """
    user_model = decode_jwt_token(token)
    user = User.select().where(User.username == user_model.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
