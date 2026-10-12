from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.core.logging import log
from backend.core.models import PagedResult, PaginationParams
from backend.modules.metrics.dependencies import MetricServiceDep
from backend.modules.metrics.domain.commands import MetricQuery
from backend.modules.metrics.schemas import (
    MetricCreateRequest,
    MetricResponse,
)

router = APIRouter(prefix="/metrics", tags=["metrics"])


def _parse_tags(tags: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for entry in tags or []:
        key, _, value = entry.partition(":")
        parsed[key] = value
    return parsed


@router.post("", response_model=MetricResponse, status_code=201)
async def create_metric(
    payload: MetricCreateRequest,
    service: MetricServiceDep,
) -> MetricResponse:
    log.info("metric.create.request", name=payload.name, value=payload.value)
    metric = await service.create(payload.to_domain())
    return MetricResponse.from_domain(metric)


@router.get("", response_model=PagedResult[MetricResponse])
async def find_metrics(
    service: MetricServiceDep,
    start_date: datetime,
    end_date: datetime,
    pagination: Annotated[PaginationParams, Depends()],
    name: Annotated[
        str | None, Query(description="Filtro opcional por nombre exacto de la métrica")
    ] = None,
    tag: Annotated[
        list[str] | None,
        Query(description="Filtro por tag en formato key:value, repetible"),
    ] = None,
) -> PagedResult[MetricResponse]:
    log.info(
        "metric.find.request",
        start_date=start_date,
        end_date=end_date,
        name=name,
        page=pagination.page,
        size=pagination.size,
    )
    query = MetricQuery(
        tags=_parse_tags(tag),
        start_date=start_date,
        end_date=end_date,
        name=name,
        page=pagination.page,
        size=pagination.size,
    )
    result = await service.find_by_tags_and_date_range(query)
    return PagedResult(
        page=result.page,
        total_items=result.total_items,
        size=result.size,
        items=[MetricResponse.from_domain(metric) for metric in result.items],
    )
