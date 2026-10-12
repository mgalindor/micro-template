import pytest

from backend.modules.users.auth_service import AuthService
from backend.modules.users.domain.commands import Credentials, UserCreate
from backend.modules.users.domain.exceptions import (
    InvalidCredentialsError,
    UserDisabledError,
)
from backend.modules.users.service import UserService
from tests.fakes import FakeRoleRepository, FakeUserRepository


async def test_authenticate_returns_token_for_valid_credentials() -> None:
    repository = FakeUserRepository()
    user_service = UserService(repository, FakeRoleRepository())
    await user_service.create(UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[]))
    auth_service = AuthService(repository)

    token = await auth_service.authenticate(Credentials(username="jdoe", password="s3cr3t12"))

    assert token


async def test_authenticate_rejects_invalid_password() -> None:
    repository = FakeUserRepository()
    user_service = UserService(repository, FakeRoleRepository())
    await user_service.create(UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[]))
    auth_service = AuthService(repository)

    with pytest.raises(InvalidCredentialsError):
        await auth_service.authenticate(Credentials(username="jdoe", password="wrong"))


async def test_authenticate_rejects_unknown_username() -> None:
    repository = FakeUserRepository()
    auth_service = AuthService(repository)

    with pytest.raises(InvalidCredentialsError):
        await auth_service.authenticate(Credentials(username="ghost", password="whatever"))


async def test_authenticate_rejects_disabled_user() -> None:
    repository = FakeUserRepository()
    user_service = UserService(repository, FakeRoleRepository())
    user = await user_service.create(
        UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[])
    )
    assert user.id is not None
    await user_service.disable(user.id)
    auth_service = AuthService(repository)

    with pytest.raises(UserDisabledError):
        await auth_service.authenticate(Credentials(username="jdoe", password="s3cr3t12"))
