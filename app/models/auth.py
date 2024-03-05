from pydantic import BaseModel, Field


class Token(BaseModel):
    """
        Base Pydantic model for token response
    """
    access_token: str = Field(...,
                              example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwOTYyMTUxN30.irqAal44EZmrDXbg0Den_QWNsXiIrznAS19Ohq2ucEk")
    refresh_token: str = Field(...,
                               example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxMDIyMjcxN30.7--478sLORNL13D7fzIsxAf8W5QyuWkOhsdAwtahmbQ")


class TokenData(BaseModel):
    """
        Base Pydantic model for token data
    """
    username: str | None = None
