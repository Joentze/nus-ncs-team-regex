"""typings for prompt"""
from pydantic import BaseModel, Field
from schemas.QueryRole import QueryRoleType
from typing import Optional


class Prompt(BaseModel):
    """type for Prompt"""
    role: QueryRoleType = Field(...)
    content: str = Field(...)

    class Config:
        extra = "allow"
