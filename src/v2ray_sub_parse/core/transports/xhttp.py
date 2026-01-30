from ..base import Base
import enum
import typing
import pydantic
if typing.TYPE_CHECKING:
    from ..stream_settings import TLSObject, SecurityEnum, RealityObject


class XhttpModeEnum(enum.Enum):
    STREAM_UP = "stream-up"
    STREAM_ONE = "stream-one"
    PACKET_UP = "packet-up"
    AUTO = "auto"


class XhttpDownloadSettingsObject():
    address: str | None = None
    port: int | None = None
    network: typing.Literal["xhttp"] = "xhttp"
    security: SecurityEnum | None = None
    tls_settings: TLSObject | None = None
    reality_settings: RealityObject | None = None
    xhttp_settings: XhttpObject | None = None

    @pydantic.model_serializer(mode='wrap')
    def custom_dump(self, handler: pydantic.SerializerFunctionWrapHandler) -> dict[str, typing.Any]:
        dumped_data = handler(self)

        dumped_data.get('xhttpSettings', {}).get(
            'extra', {}).pop('downloadSettings', None)

        return dumped_data


class XhttpMuxObject(Base):
    max_concurrency: str | None = None
    max_connections: int | None = None
    c_max_reuse_times: int | None = None
    h_max_request_times: str | None = None
    h_max_reusable_secs: str | None = None
    h_keep_alive_period: int | None = None


class XhttpExtraObject(Base):
    headers: dict[str, str] | None = None
    x_padding_bytes: str | None = None
    no_GRPC_header: bool | None = None
    sc_max_each_post_bytes: int | None = None
    sc_min_posts_interval_ms: int | None = None
    xmux: XhttpMuxObject | None = None
    download_settings: None = None


class XhttpObject(Base):
    host: str | None = None
    path: str | None = None
    mode: XhttpModeEnum | None = None
    extra: XhttpExtraObject | None = None
