class DomainError(Exception):
    """Base para todos los errores de negocio del dominio."""


class ResourceNotFoundError(DomainError):
    """Recurso genérico no encontrado, identificable por id y nombre."""

    def __init__(self, resource_id: str | int, resource_name: str) -> None:
        self.resource_id = resource_id
        self.resource_name = resource_name
        super().__init__(f"{resource_name} {resource_id} not found")


class BusinessError(DomainError):
    """Violación genérica de una regla de negocio, identificada por un código."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Business rule violation: {code}")


class AuthenticationError(DomainError):
    """Credenciales inválidas, token inválido/expirado o cuenta deshabilitada. -> 401."""


class AuthorizationError(DomainError):
    """El llamante está autenticado pero no tiene permiso para la acción. -> 403."""
