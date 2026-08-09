from collections.abc import Sequence

from src.domain.dtos.message import MessageDTO, SendMessageDTO
from src.domain.entities.message import Message
from src.services.interfaces.uow import IUnitOfWork


from src.services.ws_manager import ConnectionManager


class MessageService:
    def __init__(self, ws_manager: ConnectionManager):
        self.ws_manager = ws_manager

    async def send_message(
        self, uow: IUnitOfWork, sender_login: str, dto: SendMessageDTO
    ) -> MessageDTO:
        message = Message.create(
            sender_login=sender_login,
            recipient_login=dto.recipient_login,
            ciphertext=dto.ciphertext,
            nonce=dto.nonce,
        )
        async with uow:
            saved_message = await uow.message_repository.add(message)
            await uow.commit()

        return MessageDTO(
            id=str(saved_message.id),
            sender_login=saved_message.sender_login,
            recipient_login=saved_message.recipient_login,
            timestamp=int(saved_message.created_at.timestamp()),
            ciphertext=saved_message.ciphertext,
            nonce=saved_message.nonce,
        )

    async def get_chat_history(
        self, uow: IUnitOfWork, user1: str, user2: str, limit: int = 50, offset: int = 0
    ) -> Sequence[MessageDTO]:
        async with uow:
            messages = await uow.message_repository.get_history(
                user1=user1, user2=user2, limit=limit, offset=offset
            )

            return [
                MessageDTO(
                    id=str(msg.id),
                    sender_login=msg.sender_login,
                    recipient_login=msg.recipient_login,
                    timestamp=int(msg.created_at.timestamp()),
                    ciphertext=msg.ciphertext,
                    nonce=msg.nonce,
                )
                for msg in messages
            ]
