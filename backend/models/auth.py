from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class _EmailIn(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

class RegisterIn(_EmailIn):
    password: str = Field(min_length=8, max_length=72)


class LoginIn(_EmailIn):
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
