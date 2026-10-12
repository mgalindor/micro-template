from sqlalchemy import cast, func, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logging import log
from backend.core.models import PagedResult
from backend.modules.metrics.domain.commands import MetricCreate, MetricQuery
from backend.modules.metrics.domain.models import Metric
from backend.modules.metrics.orm import MetricORM


class MetricRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, command: MetricCreate) -> Metric:
        log.debug("metric.repository.create", name=command.name, value=command.value)
        orm = MetricORM(
            name=command.name,
            value=command.value,
            tags=command.tags,
            recorded_at=command.recorded_at,
        )
        async with self._session.begin():
            self._session.add(orm)
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def find_by_tags_and_date_range(
        self, query: MetricQuery
    ) -> PagedResult[Metric]:
        log.debug(
            "metric.repository.find",
            start_date=query.start_date,
            end_date=query.end_date,
            name=query.name,
            page=query.page,
            size=query.size,
        )
        filters = [
            MetricORM.recorded_at >= query.start_date,
            MetricORM.recorded_at <= query.end_date,
        ]
        if query.name is not None:
            filters.append(MetricORM.name == query.name)
        if query.tags:
            # Containment JSONB: la fila debe incluir todos los pares key/value pedidos.
            filters.append(MetricORM.tags.op("@>")(cast(query.tags, JSONB)))

        count_stmt = select(func.count()).select_from(MetricORM).where(*filters)
        total_items = (await self._session.execute(count_stmt)).scalar_one()

        stmt = (
            select(MetricORM)
            .where(*filters)
            .order_by(MetricORM.recorded_at)
            .offset((query.page - 1) * query.size)
            .limit(query.size)
        )
        result = await self._session.execute(stmt)
        items = [self._to_domain(orm) for orm in result.scalars().all()]
        return PagedResult(
            items=items, total_items=total_items, page=query.page, size=query.size
        )

    @staticmethod
    def _to_domain(orm: MetricORM) -> Metric:
        return Metric(
            id=orm.id,
            name=orm.name,
            value=orm.value,
            tags=orm.tags,
            recorded_at=orm.recorded_at,
            created_at=orm.created_at,
        )
