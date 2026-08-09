from pydantic import BaseModel

class SendMessageDTO(BaseModel):
    recipient_login: str
    ciphertext: str
    nonce: str

class MessageDTO(BaseModel):
    id: str
    sender_login: str
    recipient_login: str
    timestamp: int
    ciphertext: str
    nonce: str
