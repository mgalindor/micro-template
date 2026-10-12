from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_db
from backend.modules.metrics.repository import MetricRepository
from backend.modules.metrics.service import MetricService

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_metric_repository(session: SessionDep) -> MetricRepository:
    return MetricRepository(session)


MetricRepositoryDep = Annotated[MetricRepository, Depends(get_metric_repository)]


def get_metric_service(repository: MetricRepositoryDep) -> MetricService:
    return MetricService(repository)


MetricServiceDep = Annotated[MetricService, Depends(get_metric_service)]
