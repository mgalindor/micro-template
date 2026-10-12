from datetime import UTC, datetime, timedelta

import pytest

from backend.core.exceptions import ResourceNotFoundError
from backend.modules.traces.domain.commands import TraceCreate
from backend.modules.traces.domain.models import SpanStatus
from backend.modules.traces.service import TraceService
from tests.fakes import FakeTraceRepository


def _now() -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC)


async def test_create_trace_computes_duration() -> None:
    service = TraceService(FakeTraceRepository())
    start = _now()
    end = start + timedelta(milliseconds=250)

    trace = await service.create(
        TraceCreate(
            trace_id="trace-1",
            span_id="span-1",
            parent_span_id=None,
            span_name="GET /metrics",
            service_name="metrics-collector",
            start_time=start,
            end_time=end,
            status=SpanStatus.OK,
            attributes={"http.method": "GET"},
        )
    )

    assert trace.duration_ms == pytest.approx(250.0)
    assert trace.status == SpanStatus.OK


async def test_find_by_trace_id_returns_all_spans() -> None:
    service = TraceService(FakeTraceRepository())
    for span_id in ("span-1", "span-2"):
        await service.create(
            TraceCreate(
                trace_id="trace-1",
                span_id=span_id,
                parent_span_id=None,
                span_name="op",
                service_name="metrics-collector",
                start_time=_now(),
                end_time=None,
                status=SpanStatus.UNSET,
                attributes={},
            )
        )

    result = await service.find_by_trace_id("trace-1")

    assert {span.span_id for span in result.items} == {"span-1", "span-2"}
    assert result.total_items == 2


async def test_find_by_trace_id_raises_when_not_found() -> None:
    service = TraceService(FakeTraceRepository())

    with pytest.raises(ResourceNotFoundError):
        await service.find_by_trace_id("missing-trace")
