from dataclasses import dataclass
from typing import Annotated, Any, Literal

from fastapi import Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, PositiveInt, StringConstraints
from pydantic.alias_generators import to_camel

PROBLEM_JSON_MEDIA_TYPE = "application/problem+json"


class CoreModel(BaseModel):
    """
    This class add default configuration to the models
    - serialize the result to camel case
    - populate by name(true) - allow to populate the model from a dictionary with the same keys as the model attributes
      also allow to populate the model using the alias (which is in camel case)
    - from_attributes(true) - allow to populate the model from other class attributes, this allows the model receive
      other class instances in the constructor
    - loc_by_alias(true) - when error indicates the alias to make easy clients identify the error
    - ser_json_timedelta(true) - serialize the timedelta to json with ISO 8601 format
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        loc_by_alias=True,
        ser_json_timedelta="iso8601",
        extra="forbid",
    )


@dataclass(kw_only=True, slots=True, frozen=True)
class PaginationParams:
    """Typical page/size/order query params, usable as a FastAPI dependency."""

    page: Annotated[
        PositiveInt,
        Query(
            description="Page number to retrieve (1-based).",
            examples=[1],
        ),
    ] = 1
    size: Annotated[
        PositiveInt,
        Query(
            le=100,
            description="Number of items per page. Maximum of 100.",
            examples=[20],
        ),
    ] = 20
    order: Annotated[
        str | None,
        StringConstraints(strip_whitespace=True),
        Query(
            description="Comma-separated list of fields to sort by. Prefix a field "
            "with '-' for descending order (e.g. 'name,-created_at').",
            examples=["name", "-created_at", "name,-created_at"],
        ),
    ] = None

    @property
    def offset(self) -> int:
        """Number of records to skip, derived from page and size."""
        return (self.page - 1) * self.size

    @property
    def order_by(self) -> list[tuple[str, Literal["asc", "desc"]]]:
        """Parses `order` into (field, direction) pairs for building ORDER BY clauses."""
        if not self.order:
            return []
        clauses: list[tuple[str, Literal["asc", "desc"]]] = []
        for raw_field in self.order.split(","):
            field = raw_field.strip()
            if not field:
                continue
            if field.startswith("-"):
                clauses.append((field[1:], "desc"))
            else:
                clauses.append((field, "asc"))
        return clauses


@dataclass(frozen=True, slots=True)
class PagedResult[ItemT]:
    """Generic paginated result, used both between layers and as the HTTP response."""

    items: list[ItemT]
    total_items: int
    page: int
    size: int


class ProblemDetail(CoreModel):
    """RFC 7807 - Problem Details for HTTP APIs."""

    type: str = Field(default="about:blank")
    title: str
    status: int
    detail: str
    instance: str


def problem_response(
    request: Request,
    status_code: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    **extensions: Any,
) -> JSONResponse:
    problem = ProblemDetail(
        type=type_,
        title=title,
        status=status_code,
        detail=detail,
        instance=request.url.path,
    )
    content: dict[str, Any] = problem.model_dump()
    content.update(extensions)
    return JSONResponse(
        status_code=status_code,
        content=content,
        media_type=PROBLEM_JSON_MEDIA_TYPE,
    )
