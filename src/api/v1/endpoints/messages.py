from collections.abc import Sequence
import json

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.core.metrics import TYPING_EVENTS_TOTAL

from src.api.v1.depends import get_current_user_login, get_ws_user_login
from src.domain.dtos.message import MessageDTO, SendMessageDTO
from src.services.interfaces.uow import IUnitOfWork
from src.services.message import MessageService
from src.services.ws_manager import ConnectionManager

router = APIRouter(prefix="/messages", tags=["Messages"], route_class=DishkaRoute)

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
):
    login = await get_ws_user_login(token)
    if not login:
        await websocket.close(code=1008)
        return

    # WebSockets don't work well with FromDishka in route signature due to FastAPI validation
    container = websocket.app.state.dishka_container
    ws_manager = await container.get(ConnectionManager)

    await ws_manager.connect(websocket, login)
    try:
        while True:
            text = await websocket.receive_text()
            try:
                data = json.loads(text)
                if data.get("type") == "typing":
                    TYPING_EVENTS_TOTAL.inc()
                    recipient = data.get("recipient_login")
                    if recipient:
                        await ws_manager.send_personal_message(
                            {"type": "typing", "sender": login}, 
                            recipient
                        )
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, login)


@router.post("/", response_model=MessageDTO)
async def send_message(
    dto: SendMessageDTO,
    uow: FromDishka[IUnitOfWork],
    message_service: FromDishka[MessageService],
    ws_manager: FromDishka[ConnectionManager],
    sender_login: str = Depends(get_current_user_login),
) -> MessageDTO:
    msg_dto = await message_service.send_message(uow, sender_login, dto)
    await ws_manager.send_personal_message(msg_dto.model_dump(), dto.recipient_login)
    return msg_dto


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
