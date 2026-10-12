from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.modules.traces.domain.commands import TraceCreate
from backend.modules.traces.domain.models import SpanStatus, Trace


class TraceCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    span_name: str
    service_name: str
    start_time: datetime
    end_time: datetime | None = None
    status: SpanStatus = SpanStatus.UNSET
    attributes: dict[str, str] = Field(default_factory=dict)

    def to_domain(self) -> TraceCreate:
        return TraceCreate(
            trace_id=self.trace_id,
            span_id=self.span_id,
            parent_span_id=self.parent_span_id,
            span_name=self.span_name,
            service_name=self.service_name,
            start_time=self.start_time,
            end_time=self.end_time,
            status=self.status,
            attributes=self.attributes,
        )


class TraceResponse(BaseModel):
    id: int
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

    @classmethod
    def from_domain(cls, trace: Trace) -> "TraceResponse":
        assert trace.id is not None  # siempre persistido antes de responder
        return cls(
            id=trace.id,
            trace_id=trace.trace_id,
            span_id=trace.span_id,
            parent_span_id=trace.parent_span_id,
            span_name=trace.span_name,
            service_name=trace.service_name,
            start_time=trace.start_time,
            end_time=trace.end_time,
            duration_ms=trace.duration_ms,
            status=trace.status,
            attributes=trace.attributes,
            created_at=trace.created_at,
        )
