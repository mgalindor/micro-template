from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field

from backend.core.models import CoreModel
from backend.modules.users.domain.commands import UserCreate, UserUpdate
from backend.modules.users.domain.models import User


class TokenResponse(CoreModel):
    access_token: str
    token_type: str = "bearer"


class UserCreateRequest(CoreModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=1, max_length=30)
    email: EmailStr | None = None
    password: str = Field(min_length=8)
    roles: list[str] = Field(default_factory=list)

    def to_domain(self) -> UserCreate:
        return UserCreate(
            username=self.username,
            email=self.email,
            password=self.password,
            roles=self.roles,
        )


class UserUpdateRequest(CoreModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    current_password: str | None = None
    roles: list[str] | None = None

    def to_domain(self) -> UserUpdate:
        return UserUpdate(
            email=self.email,
            password=self.password,
            current_password=self.current_password,
            roles=self.roles,
        )


class UserResponse(CoreModel):
    id: int
    username: str
    email: str | None
    roles: list[str]
    is_active: bool
    created_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        assert user.id is not None  # siempre persistido antes de responder
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            roles=user.role_names,
            is_active=user.is_active,
            created_at=user.created_at,
        )
