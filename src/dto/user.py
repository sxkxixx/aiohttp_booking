from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, Field

__all__ = [
    'UserResponseDTO',
    'UserAuthRequest',
    'Token',
    'TokenResponse'
]


class UserAuthRequest(BaseModel):
    email: EmailStr
    hashed_password: str = Field(..., alias='password')

    @field_validator('email')
    @classmethod
    def email_lower(cls, field: EmailStr) -> str:
        return field.lower()

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, field: str) -> str:
        if len(field) < 6:
            raise ValueError('Password must be at least 6')
        return field


class UserResponseDTO(BaseModel):
    id: int
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    header: str


class Token(BaseModel):
    email: EmailStr
    token_type: str
    expires_in: Optional[int] = None
