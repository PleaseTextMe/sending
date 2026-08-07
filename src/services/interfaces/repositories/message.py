from abc import ABC, abstractmethod
from collections.abc import Sequence

from src.domain.entities.message import Message


class IMessageRepository(ABC):
    @abstractmethod
    async def add(self, message: Message) -> None:
        pass

    @abstractmethod
    async def get_history(self, user1: str, user2: str, limit: int = 50, offset: int = 0) -> Sequence[Message]:
        pass
