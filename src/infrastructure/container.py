from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db import postgres
from src.infrastructure.uow import SQLAlchemyUnitOfWork
from src.services.interfaces.uow import IUnitOfWork
from src.services.message import MessageService
from src.services.ws_manager import ConnectionManager


class Container(Provider):
    @provide(scope=Scope.APP)
    def provide_ws_manager(self) -> ConnectionManager:
        return ConnectionManager()

    @provide(scope=Scope.REQUEST)
    async def provide_session(self) -> AsyncIterable[AsyncSession]:
        if postgres.session_maker is None:
            raise RuntimeError("Session maker is not initialized")
        async with postgres.session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_uow(self, session: AsyncSession) -> IUnitOfWork:
        return SQLAlchemyUnitOfWork(session)

    @provide(scope=Scope.REQUEST)
    async def provide_message_service(self, ws_manager: ConnectionManager) -> MessageService:
        return MessageService(ws_manager=ws_manager)
