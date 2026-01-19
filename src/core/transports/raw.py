import dataclasses
from ..base import Base


class NoneHeaderObject(Base):
    type: str = "none"


@dataclasses.dataclass
class HTTPRequestObject(Base):
    version: str | None = None
    method: str | None = None
    path: list[str] | None = None
    headers: dict[str, list[str]] | None = None


@dataclasses.dataclass
class HTTPResponseObject(Base):
    version: str | None = None
    status: str | None = None
    reason: str | None = None
    headers: dict[str, list[str]] | None = None


@dataclasses.dataclass
class HttpHeaderObject(Base):
    type: str = dataclasses.field(default="http", init=False)
    request: HTTPRequestObject | None = None
    response: HTTPResponseObject | None = None


@dataclasses.dataclass
class RawObject(Base):
    '''RawObject соответствует элементу rawSettings в конфигурации транспорта.'''
    header: NoneHeaderObject | HttpHeaderObject | None = None
