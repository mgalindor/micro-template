"""Fakes de repositorios para tests unitarios de servicios (sin I/O real)."""

from backend.core.models import PagedResult
from backend.modules.metrics.domain.commands import MetricCreate, MetricQuery
from backend.modules.metrics.domain.models import Metric
from backend.modules.traces.domain.commands import TraceCreate
from backend.modules.traces.domain.models import Trace


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
