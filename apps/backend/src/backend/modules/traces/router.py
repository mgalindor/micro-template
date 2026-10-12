from typing import Annotated

from fastapi import APIRouter, Depends

from backend.core.logging import log
from backend.core.models import PagedResult, PaginationParams
from backend.modules.traces.dependencies import TraceServiceDep
from backend.modules.traces.schemas import TraceCreateRequest, TraceResponse

router = APIRouter(prefix="/traces", tags=["traces"])


@router.post("", response_model=TraceResponse, status_code=201)
async def create_trace(
    payload: TraceCreateRequest,
    service: TraceServiceDep,
) -> TraceResponse:
    log.info("trace.create.request", trace_id=payload.trace_id, span_id=payload.span_id)
    trace = await service.create(payload.to_domain())
    return TraceResponse.from_domain(trace)


@router.get("/{trace_id}", response_model=PagedResult[TraceResponse])
async def find_trace_by_id(
    trace_id: str,
    service: TraceServiceDep,
    pagination: Annotated[PaginationParams, Depends()],
) -> PagedResult[TraceResponse]:
    log.info(
        "trace.find.request",
        trace_id=trace_id,
        page=pagination.page,
        size=pagination.size,
    )
    result = await service.find_by_trace_id(trace_id, pagination.page, pagination.size)
    return PagedResult(
        page=result.page,
        total_items=result.total_items,
        size=result.size,
        items=[TraceResponse.from_domain(span) for span in result.items],
    )
