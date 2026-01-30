from .base import Base
from .transports.raw import RawObject
from .transports.xhttp import XhttpObject
import enum
import pydantic


class FingerprintEnum(enum.StrEnum):
    '''
    Отпечатки TLS последних версий популярных браузеров, включая:
    "chrome"
    "firefox"
    "safari"
    "ios"
    "android"
    "edge"
    "360"
    "qq"
    Автоматическая генерация отпечатка при запуске Xray:
    "random": случайный выбор из новых версий браузеров.
    "randomized": полная случайная генерация уникального отпечатка (100% поддержка TLS 1.3 с использованием X25519)
    Использование имени переменной отпечатка uTLS, например, "HelloRandomizedNoALPN" "HelloChrome_106_Shuffle". Полный список см. в библиотеке uTLS.

    Отключение эмуляции отпечатка TLS Client Hello

    DANGER

    Из соображений безопасности этот параметр не следует устанавливать в значение unsafe.

    "unsafe": отпечаток go/tls
    '''
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"
    IOS = "ios"
    ANDROID = "android"
    EDGE = "edge"
    _360 = "360"
    QQ = "qq"
    RANDOM = "random"
    RANDOMIZED = "randomized"
    UNSAFE = "unsafe"


class AlpnEnum(Base):
    '''
    Массив строк, указывающий значения ALPN, указанные во время рукопожатия TLS. Значение по умолчанию: ["h2", "http/1.1"].

    Специальное значение: ["FromMitM"] (когда это единственный элемент) заставит исходящий TLS использовать ALPN из TLS-соединения, расшифрованного входящим dokodemo-door.
    '''
    h1: bool = False
    h2: bool = False
    h3: bool = False
    from_mitm: bool = False

    @classmethod
    def from_string(cls, string: str):
        if "FromMitM" == string:
            return cls(from_mitm=True)
        h1, h2, h3 = False, False, False
        if "http/1.1" in string:
            h1 = True
        if "h2" in string:
            h2 = True
        if "h3" in string:
            h3 = True
        return cls(h1=h1, h2=h2, h3=h3)

    def to_list(self) -> list[str]:
        if self.from_mitm:
            return ["FromMitM"]
        alpn_list: list[str] = []
        if self.h2:
            alpn_list.append("h2")
        if self.h1:
            alpn_list.append("http/1.1")
        if self.h3:
            alpn_list.append("h3")
        return alpn_list

    @pydantic.model_serializer(mode='plain')
    def serialize_as_list(self) -> list[str]:
        return self.to_list()


class TLSObject(Base):
    server_name: str | None = None
    allow_insecure: bool | None = None
    alpn: AlpnEnum | None = None
    fingerprint: FingerprintEnum | None = None


class RealityObject(Base):
    server_name: str | None = None
    fingerprint: FingerprintEnum | None = None
    short_id: str | None = None
    public_key: str | None = None
    mldsa65_verify: str | None = None
    spider_x: str | None = None


class NetworkEnum(enum.StrEnum):
    '''
    network: "raw" | "xhttp" | "kcp" | "grpc" | "ws" | "httpupgrade"

    Тип способа передачи, используемого потоком данных соединения, по умолчанию "raw".
    '''
    RAW = "raw"
    TCP = "tcp"
    XHTTP = "xhttp"
    KCP = "kcp"
    GRPC = "grpc"
    WS = "ws"
    HTTPUPGRADE = "httpupgrade"


class SecurityEnum(enum.Enum):
    '''
    security: "none" | "tls" | "reality"

    Включено ли шифрование транспортного уровня, поддерживаемые опции:

    "none" означает отсутствие шифрования (значение по умолчанию)
    "tls" означает использование TLS.
    "reality" означает использование REALITY.
    '''
    NONE = "none"
    TLS = "tls"
    REALITY = "reality"


class StreamSettingsObject(Base):
    network: NetworkEnum = NetworkEnum.RAW
    security: SecurityEnum = SecurityEnum.NONE
    tls_settings: TLSObject | None = None
    reality_settings: RealityObject | None = None
    raw_settings: RawObject | None = None
    xhttp_settings: XhttpObject | None = None
    kcp_settings: None = None
    grpc_settings: None = None
    ws_settings: None = None
    httpupgrade_setting: None = None
