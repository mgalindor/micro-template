from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class MetricCreate:
    name: str
    value: float
    tags: dict[str, str]
    recorded_at: datetime


@dataclass(frozen=True, slots=True)
class MetricQuery:
    tags: dict[str, str]
    start_date: datetime
    end_date: datetime
    name: str | None = None
    page: int = 1
    size: int = 20
