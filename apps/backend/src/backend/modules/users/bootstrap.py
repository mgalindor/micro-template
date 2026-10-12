"""Ensures the default admin role and user exist on application startup."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.logging import log
from backend.modules.users.orm import RoleORM, UserORM

ADMIN_ROLE_NAME = "admin"
ADMIN_ROLE_PERMISSIONS = ["*"]


async def ensure_admin_user(session: AsyncSession) -> None:
    admin_role = await _ensure_admin_role(session)

    if not settings.admin.password_hash:
        log.warning("admin.bootstrap.skipped", reason="missing_password_hash")
        return

    stmt = select(UserORM).where(UserORM.username == settings.admin.username)
    existing_admin = (await session.execute(stmt)).scalar_one_or_none()
    if existing_admin is not None:
        log.info("admin.bootstrap.already_exists", username=settings.admin.username)
        return

    session.add(
        UserORM(
            username=settings.admin.username,
            email=None,
            password_hash=settings.admin.password_hash,
            is_active=True,
            roles=[admin_role],
        )
    )
    log.info("admin.bootstrap.created", username=settings.admin.username)


async def _ensure_admin_role(session: AsyncSession) -> RoleORM:
    stmt = select(RoleORM).where(RoleORM.name == ADMIN_ROLE_NAME)
    role = (await session.execute(stmt)).scalar_one_or_none()
    if role is None:
        role = RoleORM(name=ADMIN_ROLE_NAME, permissions=ADMIN_ROLE_PERMISSIONS)
        session.add(role)
        await session.flush()
        log.info("admin.bootstrap.role_created", role_name=ADMIN_ROLE_NAME)
    return role
