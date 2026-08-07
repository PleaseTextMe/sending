from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from src.core.utils.snowflake import generate_snowflake_id
from src.domain.entities.mixins import DateTimeMixin

class Message(DateTimeMixin, BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(default_factory=generate_snowflake_id)
    sender_login: str
    recipient_login: str
    ciphertext: str
    nonce: str
    
    @classmethod
    def create(
        cls,
        sender_login: str,
        recipient_login: str,
        ciphertext: str,
        nonce: str,
    ) -> "Message":
        return cls(
            id=generate_snowflake_id(),
            sender_login=sender_login,
            recipient_login=recipient_login,
            ciphertext=ciphertext,
            nonce=nonce,
        )
