from bcrypt import checkpw
from fastapi import APIRouter, HTTPException, Depends

from app.auth import generate_tokens, decode_jwt_token, oauth2_scheme
from app.models import SignupRequest, User, LoginRequest, Token

auth_router = APIRouter()


@auth_router.post("/auth", tags=['Auth'])
async def auth(login_request: LoginRequest) -> Token:
    """
        Endpoint for authenticating a user.

        Args:
            login_request (LoginRequest): The request object containing the user's login credentials.

        Returns:
            Token: A token for the authenticated user.
    """

    username = login_request.username
    password = login_request.password

    user = User.select().where(User.username == username).first()

    if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return generate_tokens(username=username)


@auth_router.post("/signup", tags=['Auth'])
async def signup(signup_request: SignupRequest) -> Token:
    """
        An asynchronous function to handle user sign up.
        Takes a signup request object as input and returns a token.
    """
    User.create(**signup_request.dict())

    return generate_tokens(username=signup_request.username)


@auth_router.post("/refresh", tags=['Auth'])
async def refresh_access_token(refresh_token: str = Depends(oauth2_scheme)) -> Token:
    token_data = decode_jwt_token(refresh_token, is_refresh=True)
    return generate_tokens(username=token_data.username)
