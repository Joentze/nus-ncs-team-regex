"""typing for Conversations"""
from typing import List
from schemas.Prompt import Prompt
from pydantic import BaseModel
from beanie import Document
from pydantic import Field


class Conversation(Document):
    """type for Conversation"""
    name: str = Field(..., max_length=200)
    params: object = Field(...)
    tokens: int = Field(..., ge=0)

    def to_json(self):
        """converts to json"""
        return {"name": self.name, "params": self.params, "tokens": self.tokens}


class ConversationList(BaseModel):
    """type for conversation list"""
    data: List[Conversation]


class ConversationFull(Conversation):
    """type for ConversationFull"""
    messages: List[Prompt]
    
    def to_json(self):
        """converts to json"""
        return {"id": str(self.id), "messages": self.messages, "name": self.name, "params": self.params, "tokens": self.tokens}
