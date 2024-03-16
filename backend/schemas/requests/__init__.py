"""typing for Conversations"""
from pydantic import BaseModel, Field


class ConversationPOST(BaseModel):
    """type for ConversationPOST"""
    name: str = Field(..., max_length=200)
    model: str = Field(...)
    params: object = Field(...)


class ConversationPUT(BaseModel):
    """type for ConversationPOST"""
    name: str = Field(..., max_length=200)
    params: object = Field(...)
