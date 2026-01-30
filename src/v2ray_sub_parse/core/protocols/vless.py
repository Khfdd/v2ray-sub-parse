import enum
from ..base import Base


class VLESSFlowEnum(enum.StrEnum):
    XTLS_RPRX_VISION = "xtls-rprx-vision"
    XTLS_RPRX_VISION_UDP443 = "xtls-rprx-vision-udp443"


class UserObject(Base):
    id: str | None = None
    encryption: str = "none"
    flow: VLESSFlowEnum | None = None
    level: int | None = None


class VLESSSettingsObject(Base):
    address: str | None = None
    port: int | None = None
    users: list[UserObject] | None = None
