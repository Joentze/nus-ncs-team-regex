"""types for parameters"""
from typing import List
from pydantic import BaseModel, Field, UUID4


class IDParam(BaseModel):
    """type for IDParam"""
    id: UUID4 = Field(..., description="A unique ID string")


class SecondaryIDParam(BaseModel):
    """type for SecondaryIDParam"""
    secondary_id: UUID4 = Field(..., description="A unique ID string")


class IDListParam(BaseModel):
    """type for IDListParam"""
    ids: List[UUID4] = Field(..., description="A list of optional IDs")
