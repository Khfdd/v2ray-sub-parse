from .base import Base
from .stream_settings import StreamSettingsObject
from .protocols.vless import VLESSSettingsObject
import dataclasses
import enum


class ProtocolEnum(enum.Enum):
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


class MuxXUDPProxyUDP443Enum(enum.Enum):
    REJECT = "reject"
    ALLOW = "allow"
    SKIP = "skip"


@dataclasses.dataclass
class MuxObject(Base):
    enabled: bool = False
    concurrency: int | None = None
    xudp_concurrency: int | None = None
    xudp_proxyUDP443: MuxXUDPProxyUDP443Enum | None = None


@dataclasses.dataclass
class OutboundObject(Base):
    '''{
      "sendThrough": "0.0.0.0",
      "protocol": "название протокола",
      "settings": {},
      "tag": "тег",
      "streamSettings": {},
      "proxySettings": {
        "tag": "another-outbound-tag",
        "transportLayer": false
      },
       "mux": {},
       "targetStrategy": "AsIs"
    }'''
    send_through: str | None = None
    protocol: ProtocolEnum | None = None
    settings: VLESSSettingsObject | None = None
    tag: str | None = None
    stream_settings: StreamSettingsObject | None = None
    mux: MuxObject | None = None
