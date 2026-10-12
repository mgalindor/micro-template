import pytest

from backend.core.security import verify_password
from backend.modules.users.domain.commands import UserCreate, UserUpdate
from backend.modules.users.domain.exceptions import (
    InvalidCurrentPasswordError,
    RoleNotFoundError,
    UsernameAlreadyExistsError,
)
from backend.modules.users.domain.models import Role
from backend.modules.users.service import UserService
from tests.fakes import FakeRoleRepository, FakeUserRepository


def _service(roles: list[Role] | None = None) -> UserService:
    return UserService(FakeUserRepository(), FakeRoleRepository(roles))


async def test_create_user_hashes_password() -> None:
    service = _service()

    user = await service.create(
        UserCreate(username="jdoe", email="jdoe@example.com", password="s3cr3t12", roles=[])
    )

    assert user.id is not None
    assert user.password_hash != "s3cr3t12"
    assert verify_password("s3cr3t12", user.password_hash)


async def test_create_user_rejects_duplicate_username() -> None:
    service = _service()
    await service.create(UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[]))

    with pytest.raises(UsernameAlreadyExistsError):
        await service.create(UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[]))


async def test_create_user_rejects_unknown_role() -> None:
    service = _service()

    with pytest.raises(RoleNotFoundError):
        await service.create(
            UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=["ghost"])
        )


async def test_create_user_assigns_existing_roles() -> None:
    service = _service([Role(id=1, name="viewer", permissions=["metrics:read"])])

    user = await service.create(
        UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=["viewer"])
    )

    assert user.role_names == ["viewer"]
    assert user.permissions == ["metrics:read"]


async def test_update_self_requires_current_password() -> None:
    service = _service()
    user = await service.create(
        UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[])
    )
    assert user.id is not None

    with pytest.raises(InvalidCurrentPasswordError):
        await service.update(
            user.id,
            UserUpdate(password="newpa55word", current_password="wrong"),
            is_admin=False,
        )


async def test_update_self_with_correct_current_password() -> None:
    service = _service()
    user = await service.create(
        UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[])
    )
    assert user.id is not None

    updated = await service.update(
        user.id,
        UserUpdate(password="newpa55word", current_password="s3cr3t12"),
        is_admin=False,
    )

    assert verify_password("newpa55word", updated.password_hash)


async def test_admin_update_does_not_require_current_password() -> None:
    service = _service()
    user = await service.create(
        UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[])
    )
    assert user.id is not None

    updated = await service.update(user.id, UserUpdate(password="newpa55word"), is_admin=True)

    assert verify_password("newpa55word", updated.password_hash)


async def test_disable_user_marks_inactive() -> None:
    service = _service()
    user = await service.create(
        UserCreate(username="jdoe", email=None, password="s3cr3t12", roles=[])
    )
    assert user.id is not None

    disabled = await service.disable(user.id)

    assert disabled.is_active is False
