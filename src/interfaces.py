from typing import Optional
from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    id: str = str(uuid4())
    sender: str
    content: str
    timestamp: datetime = datetime.utcnow()
    metadata: dict[str, str] = {}


class Conversation(BaseModel):
    id: str = str(uuid4())
    messages: list[Message] = []

    def add_message(self, sender: str, content: str, metadata: Optional[dict[str, str]] = None):
        message = Message(sender=sender, content=content, metadata=metadata or {})
        self.messages.append(message)
        return message
