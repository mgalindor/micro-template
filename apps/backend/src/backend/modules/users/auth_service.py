from backend.core.logging import log
from backend.core.security import create_access_token, verify_password
from backend.modules.users.domain.commands import Credentials
from backend.modules.users.domain.exceptions import (
    InvalidCredentialsError,
    UserDisabledError,
)
from backend.modules.users.repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def authenticate(self, credentials: Credentials) -> str:
        log.info("auth.authenticate.start", username=credentials.username)
        user = await self._repository.get_by_username(credentials.username)
        if user is None or not verify_password(credentials.password, user.password_hash):
            log.warning("auth.authenticate.invalid_credentials", username=credentials.username)
            raise InvalidCredentialsError()
        if not user.is_active:
            log.warning("auth.authenticate.user_disabled", username=credentials.username)
            raise UserDisabledError()

        assert user.id is not None  # siempre persistido antes de autenticar
        token = create_access_token(
            user_id=user.id,
            username=user.username,
            roles=user.role_names,
            permissions=user.permissions,
        )
        log.info("auth.authenticate.success", username=credentials.username)
        return token
