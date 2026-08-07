from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories.message import MessageRepository
from src.services.interfaces.uow import IUnitOfWork


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._message_repository = None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.rollback()

    @property
    def message_repository(self) -> MessageRepository:
        if self._message_repository is None:
            self._message_repository = MessageRepository(self.session)
        return self._message_repository
