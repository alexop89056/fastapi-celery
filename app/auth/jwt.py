from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import TokenData, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def create_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
       Generate a JWT token based on the provided data and expiration time.
       Args:
           data (dict): The data to be encoded into the token.
           expires_delta (timedelta | None, optional): The expiration time delta. Defaults to None.
       Returns:
           str: The generated JWT token.
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict) -> str:
    """
       Generate an access token using the input data and return it as a string.
       Args:
           data (dict): The data to be used for creating the access token.
       Returns:
           str: The generated access token.
    """

    return create_jwt_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data: dict) -> str:
    """
        Creates a refresh token using the provided data dictionary and returns the generated token as a string.

        Parameters:
        - data: a dictionary containing the data for creating the refresh token

        Returns:
        - str: the generated refresh token
    """
    return create_jwt_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def decode_jwt_token(token: str, is_refresh: bool = False) -> TokenData:
    """
        Decode a JWT token and validate its expiration and payload.

        Args:
            token (str): The JWT token to be decoded.
            is_refresh (bool, optional): A flag indicating whether the token is for refresh. Defaults to False.

        Returns:
            TokenData: The decoded token data.

        Raises:
            HTTPException: If the token has expired or the credentials could not be validated.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not "exp" in payload:
            raise jwt.PyJWTError

        exp_datetime = datetime.utcfromtimestamp(payload.get('exp'))
        if exp_datetime < datetime.utcnow():
            raise jwt.ExpiredSignatureError

        return TokenData(username=payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def generate_tokens(username: str) -> Token:
    """
        Generate tokens for the given username and return a Token instance.

        :param username: The username for which tokens are being generated (str)
        :return: Token instance containing access and refresh tokens
        :rtype: Token
    """
    access_token = create_access_token({"sub": username})
    refresh_token = create_refresh_token({"sub": username})
    token_instance = Token(access_token=access_token, refresh_token=refresh_token)
    return token_instance
