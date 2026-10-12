from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Role:
    id: int | None
    name: str
    permissions: list[str]


@dataclass(frozen=True, slots=True)
class User:
    id: int | None
    username: str
    email: str | None
    password_hash: str
    is_active: bool
    roles: list[Role]
    created_at: datetime
    updated_at: datetime

    @property
    def role_names(self) -> list[str]:
        return [role.name for role in self.roles]

    @property
    def permissions(self) -> list[str]:
        seen: list[str] = []
        for role in self.roles:
            for permission in role.permissions:
                if permission not in seen:
                    seen.append(permission)
        return seen
