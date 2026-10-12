from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import TokenPayload, decode_access_token
from backend.db.session import get_db
from backend.modules.users.auth_service import AuthService
from backend.modules.users.domain.exceptions import InsufficientPermissionsError
from backend.modules.users.repository import RoleRepository, UserRepository
from backend.modules.users.service import UserService

SessionDep = Annotated[AsyncSession, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_role_repository(session: SessionDep) -> RoleRepository:
    return RoleRepository(session)


RoleRepositoryDep = Annotated[RoleRepository, Depends(get_role_repository)]


def get_user_service(
    repository: UserRepositoryDep, role_repository: RoleRepositoryDep
) -> UserService:
    return UserService(repository, role_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_auth_service(repository: UserRepositoryDep) -> AuthService:
    return AuthService(repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_current_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenPayload:
    return decode_access_token(token)


CurrentTokenDep = Annotated[TokenPayload, Depends(get_current_token)]


def require_admin(token: CurrentTokenDep) -> TokenPayload:
    if "admin" not in token.roles:
        raise InsufficientPermissionsError()
    return token


AdminTokenDep = Annotated[TokenPayload, Depends(require_admin)]
