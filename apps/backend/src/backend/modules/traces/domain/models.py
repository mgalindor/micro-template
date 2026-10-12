from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SpanStatus(str, Enum):
    UNSET = "unset"
    OK = "ok"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class Trace:
    id: int | None
    trace_id: str
    span_id: str
    parent_span_id: str | None
    span_name: str
    service_name: str
    start_time: datetime
    end_time: datetime | None
    duration_ms: float | None
    status: SpanStatus
    attributes: dict[str, str]
    created_at: datetime
