from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import ResourceNotFoundError
from backend.core.logging import log
from backend.modules.users.domain.models import Role, User
from backend.modules.users.orm import RoleORM, UserORM


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_names(self, names: list[str]) -> list[RoleORM]:
        if not names:
            return []
        stmt = select(RoleORM).where(RoleORM.name.in_(names))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> RoleORM | None:
        stmt = select(RoleORM).where(RoleORM.name == name)
        return (await self._session.execute(stmt)).scalar_one_or_none()


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(UserORM).where(UserORM.username == username)
        orm = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_domain(orm) if orm is not None else None

    async def get_by_id(self, user_id: int) -> User | None:
        orm = await self._session.get(UserORM, user_id)
        return self._to_domain(orm) if orm is not None else None

    async def create(
        self,
        *,
        username: str,
        email: str | None,
        password_hash: str,
        roles: list[RoleORM],
    ) -> User:
        log.debug("user.repository.create", username=username)
        orm = UserORM(
            username=username, email=email, password_hash=password_hash, roles=roles
        )
        async with self._session.begin():
            self._session.add(orm)
        await self._session.refresh(orm, attribute_names=["roles"])
        return self._to_domain(orm)

    async def update(
        self,
        user_id: int,
        *,
        email: str | None = None,
        password_hash: str | None = None,
        roles: list[RoleORM] | None = None,
    ) -> User:
        log.debug("user.repository.update", user_id=user_id)
        orm = await self._session.get(UserORM, user_id)
        if orm is None:
            raise ResourceNotFoundError(resource_id=user_id, resource_name="user")
        async with self._session.begin():
            if email is not None:
                orm.email = email
            if password_hash is not None:
                orm.password_hash = password_hash
            if roles is not None:
                orm.roles = roles
            self._session.add(orm)
        await self._session.refresh(orm, attribute_names=["roles"])
        return self._to_domain(orm)

    async def disable(self, user_id: int) -> User:
        log.debug("user.repository.disable", user_id=user_id)
        orm = await self._session.get(UserORM, user_id)
        if orm is None:
            raise ResourceNotFoundError(resource_id=user_id, resource_name="user")
        async with self._session.begin():
            orm.is_active = False
            self._session.add(orm)
        await self._session.refresh(orm, attribute_names=["roles"])
        return self._to_domain(orm)

    @staticmethod
    def _to_domain(orm: UserORM) -> User:
        return User(
            id=orm.id,
            username=orm.username,
            email=orm.email,
            password_hash=orm.password_hash,
            is_active=orm.is_active,
            roles=[
                Role(id=role.id, name=role.name, permissions=role.permissions)
                for role in orm.roles
            ],
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
