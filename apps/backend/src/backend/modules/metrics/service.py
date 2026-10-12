from backend.core.logging import log
from backend.core.models import PagedResult
from backend.modules.metrics.domain.commands import MetricCreate, MetricQuery
from backend.modules.metrics.domain.exceptions import InvalidDateRangeError
from backend.modules.metrics.domain.models import Metric
from backend.modules.metrics.repository import MetricRepository


class MetricService:
    def __init__(self, repository: MetricRepository) -> None:
        self._repository = repository

    async def create(self, command: MetricCreate) -> Metric:
        log.info("metric.create.start", name=command.name, value=command.value)
        metric = await self._repository.create(command)
        log.info("metric.created", metric_id=metric.id, name=metric.name)
        return metric

    async def find_by_tags_and_date_range(
        self, query: MetricQuery
    ) -> PagedResult[Metric]:
        log.info(
            "metric.find.start",
            start_date=query.start_date,
            end_date=query.end_date,
            name=query.name,
        )
        if query.start_date > query.end_date:
            log.warning(
                "metric.find.invalid_date_range",
                start_date=query.start_date,
                end_date=query.end_date,
            )
            raise InvalidDateRangeError(query.start_date, query.end_date)
        return await self._repository.find_by_tags_and_date_range(query)
