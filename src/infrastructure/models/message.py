from sqlalchemy import BigInteger, Column, String, Table, DateTime

from src.infrastructure.models.base import mapper_registry

message_table = Table(
    "messages",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True),
    Column("sender_login", String, nullable=False),
    Column("recipient_login", String, nullable=False),
    Column("ciphertext", String, nullable=False),
    Column("nonce", String, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)
