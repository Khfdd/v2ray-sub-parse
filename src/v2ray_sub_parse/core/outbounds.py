from .base import Base
from .stream_settings import StreamSettingsObject
from .protocols.vless import VLESSSettingsObject
import enum
import pydantic


class ProtocolEnum(enum.StrEnum):
    BLACKHOLE = "blackhole"
    DNS = "dns"
    FREEDOM = "freedom"
    HTTP = "http"
    LOOPBACK = "loopback"
    SHADOWSOCKS = "shadowsocks"
    SOCKS = "socks"
    TROJAN = "trojan"
    VLESS = "vless"
    VMESS = "vmess"
    WIREGUARD = "wireguard"


class MuxXUDPProxyUDP443Enum(enum.StrEnum):
    REJECT = "reject"
    ALLOW = "allow"
    SKIP = "skip"


class MuxObject(Base):
    enabled: bool = False
    concurrency: int | None = None
    xudp_concurrency: int | None = None
    xudp_proxyUDP443: MuxXUDPProxyUDP443Enum | None = None


class VnextObject(Base):
    settings: list[VLESSSettingsObject]

    @pydantic.model_serializer(mode='plain')
    def serialize_as_list(self) -> dict[str, list[VLESSSettingsObject]]:
        return {
            "vnext": [i for i in self.settings]}


class OutboundObject(Base):
    send_through: str | None = None
    protocol: ProtocolEnum | None = None
    settings: VnextObject | None = None
    tag: str | None = None
    stream_settings: StreamSettingsObject | None = None
    mux: MuxObject | None = None
