from datetime import datetime

from pydantic import ConfigDict, Field

from backend.core.models import CoreModel
from backend.modules.metrics.domain.commands import MetricCreate
from backend.modules.metrics.domain.models import Metric


class MetricCreateRequest(CoreModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=255)
    value: float
    tags: dict[str, str] = Field(min_length=1, description="Requiere al menos un tag")
    recorded_at: datetime

    def to_domain(self) -> MetricCreate:
        return MetricCreate(
            name=self.name,
            value=self.value,
            tags=self.tags,
            recorded_at=self.recorded_at,
        )


class MetricResponse(CoreModel):
    id: int
    name: str
    value: float
    tags: dict[str, str]
    recorded_at: datetime
    created_at: datetime

    @classmethod
    def from_domain(cls, metric: Metric) -> "MetricResponse":
        assert metric.id is not None  # siempre persistido antes de responder
        return cls(
            id=metric.id,
            name=metric.name,
            value=metric.value,
            tags=metric.tags,
            recorded_at=metric.recorded_at,
            created_at=metric.created_at,
        )
