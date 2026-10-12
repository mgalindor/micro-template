from backend.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BusinessError,
    ResourceNotFoundError,
)


class UsernameAlreadyExistsError(BusinessError):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(code="username_already_exists")


class InvalidCredentialsError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("Invalid username or password")


class UserDisabledError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__("User account is disabled")


class InvalidCurrentPasswordError(BusinessError):
    def __init__(self) -> None:
        super().__init__(code="invalid_current_password")


class RoleNotFoundError(ResourceNotFoundError):
    def __init__(self, name: str) -> None:
        super().__init__(resource_id=name, resource_name="role")


class InsufficientPermissionsError(AuthorizationError):
    def __init__(self) -> None:
        super().__init__("You do not have permission to perform this action")
