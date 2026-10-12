from backend.core.exceptions import ResourceNotFoundError
from backend.core.logging import log
from backend.core.models import PagedResult
from backend.modules.traces.domain.commands import TraceCreate
from backend.modules.traces.domain.models import Trace
from backend.modules.traces.repository import TraceRepository


class TraceService:
    def __init__(self, repository: TraceRepository) -> None:
        self._repository = repository

    async def create(self, command: TraceCreate) -> Trace:
        log.info(
            "trace.create.start", trace_id=command.trace_id, span_id=command.span_id
        )
        trace = await self._repository.create(command)
        log.info("trace.created", trace_id=trace.trace_id, span_id=trace.span_id)
        return trace

    async def find_by_trace_id(
        self, trace_id: str, page: int = 1, size: int = 20
    ) -> PagedResult[Trace]:
        log.info("trace.find.start", trace_id=trace_id, page=page, size=size)
        result = await self._repository.find_by_trace_id(trace_id, page, size)
        if result.total_items == 0:
            log.warning("trace.find.not_found", trace_id=trace_id)
            raise ResourceNotFoundError(resource_id=trace_id, resource_name="Trace")
        return result
