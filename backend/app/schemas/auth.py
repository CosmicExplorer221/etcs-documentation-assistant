from pydantic import BaseModel
from app.schemas.user import UserResponse


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str  # user_id
    exp: int
    type: str  # "access" or "refresh"
