from datetime import datetime

from backend.core.exceptions import DomainError


class InvalidDateRangeError(DomainError):
    def __init__(self, start_date: datetime, end_date: datetime) -> None:
        self.start_date = start_date
        self.end_date = end_date
        super().__init__(
            f"start_date {start_date.isoformat()} must not be after end_date {end_date.isoformat()}"
        )
