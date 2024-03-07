from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, Field

__all__ = [
    'UserResponseDTO',
    'UserLoginRequest',
    'Token',
    'TokenResponse',
    'UserRegisterRequest',
    'RefreshSessionRequest'
]


class RefreshSessionRequest(BaseModel):
    fingerprint: str


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(...)

    @field_validator('email', mode='before')
    @classmethod
    def email_lower(cls, field: EmailStr) -> str:
        return field.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, field: str) -> str:
        if len(field) < 6:
            raise ValueError('Password must be at least 6')
        return field


class UserLoginRequest(RefreshSessionRequest, UserRegisterRequest):
    pass


class UserResponseDTO(BaseModel):
    id: int
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    header: str


class Token(BaseModel):
    email: EmailStr
    token_type: str
    expires_in: Optional[int] = None
