from datetime import UTC, datetime, timedelta

import pytest

from backend.modules.metrics.domain.commands import MetricCreate, MetricQuery
from backend.modules.metrics.domain.exceptions import InvalidDateRangeError
from backend.modules.metrics.service import MetricService
from tests.fakes import FakeMetricRepository


def _now() -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC)


async def test_create_metric_returns_metric_with_id() -> None:
    service = MetricService(FakeMetricRepository())

    metric = await service.create(
        MetricCreate(
            name="requests.count", value=42.0, tags={"env": "prod"}, recorded_at=_now()
        )
    )

    assert metric.id is not None
    assert metric.name == "requests.count"
    assert metric.tags == {"env": "prod"}


async def test_find_by_tags_and_date_range_filters_by_tags() -> None:
    service = MetricService(FakeMetricRepository())
    await service.create(
        MetricCreate(name="cpu", value=1.0, tags={"env": "prod"}, recorded_at=_now())
    )
    await service.create(
        MetricCreate(name="cpu", value=2.0, tags={"env": "staging"}, recorded_at=_now())
    )

    result = await service.find_by_tags_and_date_range(
        MetricQuery(
            tags={"env": "prod"},
            start_date=_now() - timedelta(days=1),
            end_date=_now() + timedelta(days=1),
        )
    )

    assert result.total_items == 1
    assert len(result.items) == 1
    assert result.items[0].tags == {"env": "prod"}


async def test_find_by_tags_and_date_range_rejects_inverted_range() -> None:
    service = MetricService(FakeMetricRepository())

    with pytest.raises(InvalidDateRangeError):
        await service.find_by_tags_and_date_range(
            MetricQuery(tags={}, start_date=_now(), end_date=_now() - timedelta(days=1))
        )
