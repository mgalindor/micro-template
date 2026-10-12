"""Fakes de repositorios para tests unitarios de servicios (sin I/O real)."""

from datetime import UTC, datetime

from backend.core.models import PagedResult
from backend.modules.metrics.domain.commands import MetricCreate, MetricQuery
from backend.modules.metrics.domain.models import Metric
from backend.modules.traces.domain.commands import TraceCreate
from backend.modules.traces.domain.models import Trace
from backend.modules.users.domain.models import Role, User


class FakeMetricRepository:
    def __init__(self) -> None:
        self._items: list[Metric] = []
        self._next_id = 1

    async def create(self, command: MetricCreate) -> Metric:
        metric = Metric(
            id=self._next_id,
            name=command.name,
            value=command.value,
            tags=command.tags,
            recorded_at=command.recorded_at,
            created_at=command.recorded_at,
        )
        self._next_id += 1
        self._items.append(metric)
        return metric

    async def find_by_tags_and_date_range(
        self, query: MetricQuery
    ) -> PagedResult[Metric]:
        def matches(metric: Metric) -> bool:
            in_range = query.start_date <= metric.recorded_at <= query.end_date
            matches_name = query.name is None or metric.name == query.name
            has_tags = all(
                metric.tags.get(key) == value for key, value in query.tags.items()
            )
            return in_range and matches_name and has_tags

        matched = [metric for metric in self._items if matches(metric)]
        offset = (query.page - 1) * query.size
        page_items = matched[offset : offset + query.size]
        return PagedResult(
            items=page_items,
            total_items=len(matched),
            page=query.page,
            size=query.size,
        )


class FakeTraceRepository:
    def __init__(self) -> None:
        self._items: list[Trace] = []
        self._next_id = 1

    async def create(self, command: TraceCreate) -> Trace:
        duration_ms = None
        if command.end_time is not None:
            duration_ms = (command.end_time - command.start_time).total_seconds() * 1000

        trace = Trace(
            id=self._next_id,
            trace_id=command.trace_id,
            span_id=command.span_id,
            parent_span_id=command.parent_span_id,
            span_name=command.span_name,
            service_name=command.service_name,
            start_time=command.start_time,
            end_time=command.end_time,
            duration_ms=duration_ms,
            status=command.status,
            attributes=command.attributes,
            created_at=command.start_time,
        )
        self._next_id += 1
        self._items.append(trace)
        return trace

    async def find_by_trace_id(
        self, trace_id: str, page: int, size: int
    ) -> PagedResult[Trace]:
        matched = [trace for trace in self._items if trace.trace_id == trace_id]
        offset = (page - 1) * size
        page_items = matched[offset : offset + size]
        return PagedResult(
            items=page_items, total_items=len(matched), page=page, size=size
        )


class FakeRoleRepository:
    def __init__(self, roles: list[Role] | None = None) -> None:
        self._roles = {role.name: role for role in (roles or [])}

    async def find_by_names(self, names: list[str]) -> list[Role]:
        return [self._roles[name] for name in names if name in self._roles]

    async def get_by_name(self, name: str) -> Role | None:
        return self._roles.get(name)


class FakeUserRepository:
    def __init__(self) -> None:
        self._items: dict[int, User] = {}
        self._next_id = 1

    async def get_by_username(self, username: str) -> User | None:
        for user in self._items.values():
            if user.username == username:
                return user
        return None

    async def get_by_id(self, user_id: int) -> User | None:
        return self._items.get(user_id)

    async def create(
        self, *, username: str, email: str | None, password_hash: str, roles: list[Role]
    ) -> User:
        now = datetime.now(UTC)
        user = User(
            id=self._next_id,
            username=username,
            email=email,
            password_hash=password_hash,
            is_active=True,
            roles=list(roles),
            created_at=now,
            updated_at=now,
        )
        self._items[user.id] = user
        self._next_id += 1
        return user

    async def update(
        self,
        user_id: int,
        *,
        email: str | None = None,
        password_hash: str | None = None,
        roles: list[Role] | None = None,
    ) -> User:
        user = self._items[user_id]
        updated = User(
            id=user.id,
            username=user.username,
            email=email if email is not None else user.email,
            password_hash=password_hash if password_hash is not None else user.password_hash,
            is_active=user.is_active,
            roles=list(roles) if roles is not None else user.roles,
            created_at=user.created_at,
            updated_at=datetime.now(UTC),
        )
        self._items[user_id] = updated
        return updated

    async def disable(self, user_id: int) -> User:
        user = self._items[user_id]
        updated = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_active=False,
            roles=user.roles,
            created_at=user.created_at,
            updated_at=datetime.now(UTC),
        )
        self._items[user_id] = updated
        return updated

