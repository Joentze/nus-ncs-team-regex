"""handlers for mongodb"""
from schemas.Conversation import ConversationFull
from schemas.Prompt import Prompt
import tiktoken


async def add_to_message_history(id: str, prompt: Prompt) -> ConversationFull:
    """adds message history to the message field"""
    doc = await ConversationFull.get(id)
    return await doc.set({ConversationFull.messages: [*doc.messages, prompt]})


async def add_token_count(id: str, content: int) -> ConversationFull:
    """increases the token count of the conversation"""
    doc = await ConversationFull.get(id)
    encoder = tiktoken.get_encoding("cl100k_base")
    token_count = len(encoder.encode(content))
    return await doc.set({ConversationFull.tokens: doc.tokens+token_count})
