from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logging import log
from backend.core.models import PagedResult
from backend.modules.traces.domain.commands import TraceCreate
from backend.modules.traces.domain.models import Trace
from backend.modules.traces.orm import TraceORM


class TraceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, command: TraceCreate) -> Trace:
        log.debug(
            "trace.repository.create",
            trace_id=command.trace_id,
            span_id=command.span_id,
        )
        duration_ms = None
        if command.end_time is not None:
            duration_ms = (command.end_time - command.start_time).total_seconds() * 1000

        orm = TraceORM(
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
        )
        async with self._session.begin():
            self._session.add(orm)
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def find_by_trace_id(
        self, trace_id: str, page: int, size: int
    ) -> PagedResult[Trace]:
        log.debug(
            "trace.repository.find",
            trace_id=trace_id,
            page=page,
            size=size,
        )
        count_stmt = (
            select(func.count())
            .select_from(TraceORM)
            .where(TraceORM.trace_id == trace_id)
        )
        total_items = (await self._session.execute(count_stmt)).scalar_one()

        stmt = (
            select(TraceORM)
            .where(TraceORM.trace_id == trace_id)
            .order_by(TraceORM.start_time)
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self._session.execute(stmt)
        items = [self._to_domain(orm) for orm in result.scalars().all()]
        return PagedResult(items=items, total_items=total_items, page=page, size=size)

    @staticmethod
    def _to_domain(orm: TraceORM) -> Trace:
        return Trace(
            id=orm.id,
            trace_id=orm.trace_id,
            span_id=orm.span_id,
            parent_span_id=orm.parent_span_id,
            span_name=orm.span_name,
            service_name=orm.service_name,
            start_time=orm.start_time,
            end_time=orm.end_time,
            duration_ms=orm.duration_ms,
            status=orm.status,
            attributes=orm.attributes,
            created_at=orm.created_at,
        )
