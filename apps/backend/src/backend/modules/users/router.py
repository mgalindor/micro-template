from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.core.logging import log
from backend.modules.users.dependencies import (
    AdminTokenDep,
    AuthServiceDep,
    CurrentTokenDep,
    UserServiceDep,
)
from backend.modules.users.domain.commands import Credentials
from backend.modules.users.domain.exceptions import InsufficientPermissionsError
from backend.modules.users.schemas import (
    TokenResponse,
    UserCreateRequest,
    UserResponse,
    UserUpdateRequest,
)

router = APIRouter(tags=["users"])


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> TokenResponse:
    log.info("auth.login.request", username=form_data.username)
    token = await service.authenticate(
        Credentials(username=form_data.username, password=form_data.password)
    )
    return TokenResponse(access_token=token)


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateRequest,
    service: UserServiceDep,
    _admin: AdminTokenDep,
) -> UserResponse:
    log.info("user.create.request", username=payload.username)
    user = await service.create(payload.to_domain())
    return UserResponse.from_domain(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    service: UserServiceDep,
    token: CurrentTokenDep,
) -> UserResponse:
    is_admin = "admin" in token.roles
    if not is_admin:
        if token.user_id != user_id:
            raise InsufficientPermissionsError()
        if payload.roles is not None:
            raise InsufficientPermissionsError()

    log.info("user.update.request", user_id=user_id, is_admin=is_admin)
    user = await service.update(user_id, payload.to_domain(), is_admin=is_admin)
    return UserResponse.from_domain(user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disable_user(
    user_id: int,
    service: UserServiceDep,
    _admin: AdminTokenDep,
) -> None:
    log.info("user.disable.request", user_id=user_id)
    await service.disable(user_id)
