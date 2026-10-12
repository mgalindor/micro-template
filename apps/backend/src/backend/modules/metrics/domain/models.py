from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Metric:
    id: int | None
    name: str
    value: float
    tags: dict[str, str]
    recorded_at: datetime
    created_at: datetime
