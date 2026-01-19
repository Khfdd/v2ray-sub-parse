import dataclasses
import enum
from ..base import Base


class VLESSFlowEnum(enum.Enum):
    NONE = "none"
    XTLS_RPRX_VISION = "xtls-rprx-vision"
    XTLS_RPRX_VISION_UDP443 = "xtls-rprx-vision-udp443"


@dataclasses.dataclass
class VLESSSettingsObject(Base):
    address: str | None = None
    port: int | None = None
    id: str | None = None
    encryption: str = "none"
    flow: VLESSFlowEnum | None = None
    level: int | None = None
