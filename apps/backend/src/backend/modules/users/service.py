from backend.core.exceptions import ResourceNotFoundError
from backend.core.logging import log
from backend.core.security import hash_password, verify_password
from backend.modules.users.domain.commands import UserCreate, UserUpdate
from backend.modules.users.domain.exceptions import (
    InvalidCurrentPasswordError,
    RoleNotFoundError,
    UsernameAlreadyExistsError,
)
from backend.modules.users.domain.models import User
from backend.modules.users.orm import RoleORM
from backend.modules.users.repository import RoleRepository, UserRepository


class UserService:
    def __init__(self, repository: UserRepository, role_repository: RoleRepository) -> None:
        self._repository = repository
        self._role_repository = role_repository

    async def create(self, command: UserCreate) -> User:
        log.info("user.create.start", username=command.username)
        existing = await self._repository.get_by_username(command.username)
        if existing is not None:
            log.warning("user.create.username_taken", username=command.username)
            raise UsernameAlreadyExistsError(command.username)

        roles = await self._resolve_roles(command.roles)
        user = await self._repository.create(
            username=command.username,
            email=command.email,
            password_hash=hash_password(command.password),
            roles=roles,
        )
        log.info("user.created", user_id=user.id, username=user.username)
        return user

    async def update(self, user_id: int, command: UserUpdate, *, is_admin: bool) -> User:
        log.info("user.update.start", user_id=user_id, is_admin=is_admin)
        password_hash = None
        if command.password is not None:
            if not is_admin:
                current_user = await self._repository.get_by_id(user_id)
                if current_user is None:
                    raise ResourceNotFoundError(resource_id=user_id, resource_name="user")
                if command.current_password is None or not verify_password(
                    command.current_password, current_user.password_hash
                ):
                    log.warning("user.update.invalid_current_password", user_id=user_id)
                    raise InvalidCurrentPasswordError()
            password_hash = hash_password(command.password)

        roles = (
            await self._resolve_roles(command.roles) if command.roles is not None else None
        )

        user = await self._repository.update(
            user_id, email=command.email, password_hash=password_hash, roles=roles
        )
        log.info("user.updated", user_id=user.id)
        return user

    async def disable(self, user_id: int) -> User:
        log.info("user.disable.start", user_id=user_id)
        user = await self._repository.disable(user_id)
        log.info("user.disabled", user_id=user.id)
        return user

    async def _resolve_roles(self, names: list[str]) -> list[RoleORM]:
        if not names:
            return []
        found = await self._role_repository.find_by_names(names)
        found_names = {role.name for role in found}
        missing = [name for name in names if name not in found_names]
        if missing:
            raise RoleNotFoundError(missing[0])
        return found
