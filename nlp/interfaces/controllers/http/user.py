from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import (
    FromDishka,
    DishkaRoute
)

from nlp.application.interactors import (
    RegisterUser,
    LoginUser
)
from nlp.interfaces.dtos.user import (
    RegisterUserDTO,
    LoginUserDTO
)


user_router = APIRouter(prefix="/users", tags=["Users router"], route_class=DishkaRoute)


@user_router.post("/register")
async def register_user(
    dto: RegisterUserDTO,
    interactor: FromDishka[RegisterUser]
):
    await interactor(dto.email, dto.password)


@user_router.post("/login")
async def login_user(
    dto: LoginUserDTO,
    interactor: FromDishka[LoginUser]
):
    token = await interactor(dto.email, dto.password)
    resp = JSONResponse({"detail": "Logged in"})
    resp.set_cookie("token", token)
    return resp
