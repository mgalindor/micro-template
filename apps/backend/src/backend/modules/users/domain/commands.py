from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Credentials:
    username: str
    password: str


@dataclass(frozen=True, slots=True)
class UserCreate:
    username: str
    email: str | None
    password: str
    roles: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class UserUpdate:
    email: str | None = None
    password: str | None = None
    current_password: str | None = None
    roles: list[str] | None = None
