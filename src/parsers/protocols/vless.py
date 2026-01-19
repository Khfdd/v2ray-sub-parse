from ...core.outbounds import OutboundObject
from urllib.parse import urlparse, parse_qs
from ...core.outbounds import OutboundObject, ProtocolEnum, MuxObject, MuxXUDPProxyUDP443Enum
from ...core.stream_settings import StreamSettingsObject, NetworkEnum, SecurityEnum
from ...core.protocols.vless import VLESSSettingsObject, VLESSFlowEnum
from ...core.transports.raw import RawObject
import typing


def parse_vless(url: str) -> OutboundObject:
    """
    Пример парсера для VLESS ссылок.
    vless://uuid@ip:port?params#tag
    """

    parsed = urlparse(url)
    if parsed.scheme != "vless":
        raise ValueError("Not a VLESS URL")

    user_info = parsed.username
    host = parsed.hostname
    port = parsed.port
    query = parse_qs(parsed.query)
    tag = parsed.fragment

    def _(*args: str, default: typing.Any = None) -> typing.Any:
        for i in args:
            data = query.get(i, None)
            if data is None:
                return default
            for j in data:
                return j
        return default

    def _d(*args: str, default: typing.Any = None) -> typing.Any:
        val = _(*args, default=default)
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    settings = VLESSSettingsObject(
        address=host,
        port=port,
        id=user_info,
        encryption=_("encryption", default="none"),
        flow=VLESSFlowEnum(_("flow", default=None)),
        level=_d("level", default=None)
    )
    security = SecurityEnum(_("security", "tls", default="none"))
    tls_settings = None
    reality_settings = None
    if security == security.TLS:
        from ...core.stream_settings import TLSObject
        from ...core.stream_settings import AlpnEnum
        from ...core.stream_settings import FingerprintEnum
        tls_settings = TLSObject(
            server_name=_("server_name"),
            allow_insecure=_("allow_insecure") in ["1", "true"],
            alpn=AlpnEnum.from_string(_("alpn")),
            fingerprint=FingerprintEnum(
                _("fingerprint", "fp", default="chrome"))
        )
    elif security == security.REALITY:
        from ...core.stream_settings import RealityObject
        from ...core.stream_settings import FingerprintEnum
        reality_settings = RealityObject(
            server_name=_("server_name"),
            fingerprint=FingerprintEnum(
                _("fingerprint", "fp", default="chrome")),
            short_id=_d("short_id", "sid"),
            password=_("pubkey", "publickey", "pbk"),
            mldsa65_verify=_("mldsa65"),
            spider_x=_("spx", "spiderx")
        )
    stream_settings = StreamSettingsObject(
        network=NetworkEnum(_("type", "network", default="raw")),
        raw_settings=RawObject(),
        tls_settings=tls_settings,
        reality_settings=reality_settings
    )

    outbound = OutboundObject(
        protocol=ProtocolEnum.VLESS,
        settings=settings,
        tag=tag if tag else None,
        stream_settings=stream_settings,
        mux=MuxObject(
            enabled=_("mux", default="false").lower() in ["1", "true"],
            concurrency=_d("concurrency", default=None),
            xudp_concurrency=_d("xudp_concurrency", default=None),
            xudp_proxyUDP443=(
                MuxXUDPProxyUDP443Enum(
                    _("xudp_proxyUDP443", default="skip"))
            )
        )
    )
    return outbound
