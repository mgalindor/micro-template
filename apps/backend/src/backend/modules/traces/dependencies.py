from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_db
from backend.modules.traces.repository import TraceRepository
from backend.modules.traces.service import TraceService

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_trace_repository(session: SessionDep) -> TraceRepository:
    return TraceRepository(session)


TraceRepositoryDep = Annotated[TraceRepository, Depends(get_trace_repository)]


def get_trace_service(repository: TraceRepositoryDep) -> TraceService:
    return TraceService(repository)


TraceServiceDep = Annotated[TraceService, Depends(get_trace_service)]
