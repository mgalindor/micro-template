from dataclasses import dataclass
from datetime import datetime

from backend.modules.traces.domain.models import SpanStatus


@dataclass(frozen=True, slots=True)
class TraceCreate:
    trace_id: str
    span_id: str
    parent_span_id: str | None
    span_name: str
    service_name: str
    start_time: datetime
    end_time: datetime | None
    status: SpanStatus
    attributes: dict[str, str]
