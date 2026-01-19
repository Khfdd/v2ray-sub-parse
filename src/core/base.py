import typing
import enum
from .mixins import ToDictMixin


class Base(ToDictMixin):
    def to_dict(self) -> dict[str, typing.Any]:
        result: dict[str, typing.Any] = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Base):
                result[key] = value.to_dict()
            elif isinstance(value, enum.Enum):
                result[key] = value.value
            elif isinstance(value, list):
                result[key] = []
                for item in value:  # type: ignore
                    if isinstance(item, Base):
                        result[key].append(item.to_dict())
                    elif isinstance(item, enum.Enum):
                        result[key].append(item.value)
                    else:
                        result[key].append(item)
            else:
                result[key] = value
        return result
