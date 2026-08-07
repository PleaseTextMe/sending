from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, message: Message) -> None:
        self.session.add(message)

    async def get_history(self, user1: str, user2: str, limit: int = 50, offset: int = 0) -> Sequence[Message]:
        stmt = (
            select(Message)
            .where(
                (Message.sender_login == user1) & (Message.recipient_login == user2) |
                (Message.sender_login == user2) & (Message.recipient_login == user1)
            )
            .order_by(Message.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
