import httpx
from fastapi import Header, HTTPException

async def get_current_user_login(x_auth_token: str = Header(..., description="Auth token from auth microservice")) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "http://auth_app:8000/api/v1/auth/me/",
                headers={"x-auth-token": x_auth_token}
            )
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get("username")
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Auth service unavailable")


async def get_ws_user_login(token: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "http://auth_app:8000/api/v1/auth/me/",
                headers={"x-auth-token": token}
            )
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get("username")
            return None
        except httpx.RequestError:
            return None
