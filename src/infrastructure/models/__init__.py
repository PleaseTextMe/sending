from src.domain.entities.message import Message
from src.infrastructure.models.base import mapper_registry
from src.infrastructure.models.message import message_table


def start_mappers() -> None:
    mapper_registry.map_imperatively(Message, message_table)
