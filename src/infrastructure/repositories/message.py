from collections.abc import Sequence

from sqlalchemy import Result, and_, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.message import Message
from src.infrastructure.models.message import message_table


class MessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, message: Message) -> Message:
        insert_data = message.model_dump(exclude={"model_config"})
        query = insert(Message).values(insert_data).returning(Message)
        result: Result = await self.session.execute(query)
        db_message = result.unique().scalar_one()
        return Message.model_validate(db_message)

    async def get_history(self, user1: str, user2: str, limit: int = 50, offset: int = 0) -> Sequence[Message]:
        stmt = (
            select(Message)
            .where(
                or_(
                    and_(
                        message_table.c.sender_login == user1,
                        message_table.c.recipient_login == user2
                    ),
                    and_(
                        message_table.c.sender_login == user2,
                        message_table.c.recipient_login == user1
                    )
                )
            )
            .order_by(message_table.c.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
