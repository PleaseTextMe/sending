from collections.abc import Sequence

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from src.api.v1.depends import get_current_user_login
from src.domain.dtos.message import MessageDTO, SendMessageDTO
from src.services.interfaces.uow import IUnitOfWork
from src.services.message import MessageService

router = APIRouter(prefix="/messages", tags=["Messages"], route_class=DishkaRoute)


@router.post("/", response_model=MessageDTO)
async def send_message(
    dto: SendMessageDTO,
    uow: FromDishka[IUnitOfWork],
    message_service: FromDishka[MessageService],
    sender_login: str = Depends(get_current_user_login),
) -> MessageDTO:
    return await message_service.send_message(uow, sender_login, dto)


@router.get("/", response_model=Sequence[MessageDTO])
async def get_history(
    recipient_login: str,
    uow: FromDishka[IUnitOfWork],
    message_service: FromDishka[MessageService],
    sender_login: str = Depends(get_current_user_login),
    limit: int = 50,
    offset: int = 0,
) -> Sequence[MessageDTO]:
    return await message_service.get_chat_history(
        uow, sender_login, recipient_login, limit, offset
    )
