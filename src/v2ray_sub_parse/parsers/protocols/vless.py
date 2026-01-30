from ...core.outbounds import OutboundObject
from urllib.parse import urlparse, parse_qs
from ...core.outbounds import OutboundObject, ProtocolEnum, MuxObject, MuxXUDPProxyUDP443Enum, VnextObject
from ...core.stream_settings import StreamSettingsObject, NetworkEnum, SecurityEnum
from ...core.protocols.vless import VLESSSettingsObject, VLESSFlowEnum, UserObject
from ...core.transports.raw import RawObject
from ...core.transports.xhttp import XhttpObject, XhttpModeEnum, XhttpExtraObject
import typing
import orjson
import logging
import urllib.parse

logger = logging.getLogger(__name__)


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

    def _decode_extra(extra: str) -> XhttpExtraObject | None:
        if not extra:
            return None

        try:
            raw = urllib.parse.unquote_plus(extra)
            data = orjson.loads(raw)
            return XhttpExtraObject.model_validate(data)
        except (ValueError, orjson.JSONDecodeError) as e:
            logger.error("invalid extra payload", exc_info=e)
            return None

    def _decode_tag(tag: str | None) -> str | None:
        if tag is None:
            return None
        try:
            return urllib.parse.unquote(tag)
        except:
            return None

    def _(*args: str, default: typing.Any = None) -> typing.Any:
        res = default
        for i in args:
            data = query.get(i, None)
            if data is None:
                continue
            for j in data:
                return j
        return res

    def _d(*args: str, default: typing.Any = None) -> typing.Any:
        val = _(*args, default=default)
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    settings = VLESSSettingsObject(
        address=host,
        port=port,
        users=[
            UserObject(
                id=user_info,
                encryption=_("encryption", default="none"),
                flow=VLESSFlowEnum(_("flow")) if _("flow") else None,
                level=_d("level", default=None)
            )
        ]
    )
    security = SecurityEnum(
        _("security", "tls", default="none"))
    tls_settings = None
    reality_settings = None
    if security == security.TLS:
        from ...core.stream_settings import TLSObject
        from ...core.stream_settings import AlpnEnum
        from ...core.stream_settings import FingerprintEnum
        tls_settings = TLSObject(
            server_name=_("server_name"),
            allow_insecure=_("allow_insecure") in ["1", "true"],
            alpn=AlpnEnum.from_string(_("alpn", default="http/1.1,h2")),
            fingerprint=FingerprintEnum(
                _("fingerprint", "fp", default="chrome"))
        )
    elif security == security.REALITY:
        from ...core.stream_settings import RealityObject
        from ...core.stream_settings import FingerprintEnum
        reality_settings = RealityObject(
            server_name=_("server_name", "sni"),
            fingerprint=FingerprintEnum(
                _("fingerprint", "fp", default="chrome")),
            short_id=_("short_id", "sid"),
            public_key=_("pubkey", "publickey", "pbk"),
            mldsa65_verify=_("mldsa65"),
            spider_x=_("spx", "spiderx")
        )

    network = NetworkEnum(
        _("type", "network", default="tcp"))
    stream_settings = StreamSettingsObject(
        network=network,
        raw_settings=RawObject(

        ) if network == NetworkEnum.RAW else None,
        xhttp_settings=XhttpObject(
            host=_("host"),
            path=_("path"),
            mode=XhttpModeEnum(
                _("mode")
            ) if _("mode") else None,
            extra=_decode_extra(_("extra"))
        ) if network == NetworkEnum.XHTTP else None,
        security=security,
        tls_settings=tls_settings,
        reality_settings=reality_settings
    )

    outbound = OutboundObject(
        protocol=ProtocolEnum.VLESS,
        settings=VnextObject(settings=[settings]),
        tag=_decode_tag(tag),
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
