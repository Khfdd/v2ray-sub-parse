import collections.abc
import typing

# Импортируем наши модели (результат работы)
from ..core.outbounds import OutboundObject

# Импортируем функции-парсеры для каждого протокола
# (Предполагается, что ты их реализуешь в папке protocols/)
from ..parsers.protocols.vless import parse_vless


class ParserManager:
    """
    Класс-оркестратор. Принимает сырую строку (ссылку), 
    определяет протокол и вызывает соответствующий парсер.
    """

    # Словарь маппинга: "название протокола" -> "функция парсер"
    _HANDLERS: dict[str, collections.abc.Callable[[str], OutboundObject]] = {
        "vless": parse_vless,
    }

    @classmethod
    def parse(cls, url: str) -> OutboundObject | None:
        """
        Главный метод. Превращает одну ссылку в объект Outbound.
        """
        url = url.strip()
        if not url:
            return None

        # 1. Определяем протокол (схемa)
        # vless://uuid@ip:port... -> scheme='vless'
        try:
            # Можно использовать urlparse, но для vmess:// часто нужна ручная обработка,
            # так как vmess://ey... это не совсем валидный URL по стандартам RFC
            if "://" not in url:
                raise ValueError("Invalid URL format: missing '://'")

            scheme = url.split("://")[0].lower()
        except Exception as e:
            print(f"Error parsing scheme for URL: {url[:20]}... : {e}")
            return None

        # 2. Ищем нужный обработчик
        handler = cls._HANDLERS.get(scheme)

        if not handler:
            print(f"Unsupported protocol: {scheme}")
            return None

        # 3. Вызываем парсер и возвращаем результат (Outbound dataclass)
        try:
            return handler(url)
        except Exception as e:
            # Логируем ошибку, но не роняем весь процесс парсинга подписки
            print(f"Failed to parse {scheme} link: {e}")
            return None

    @classmethod
    def parse_as_dict(cls, url: str) -> dict[str, typing.Any]:
        t = cls.parse(
            url)
        if t is None:
            logger.error(f"Error parse %s url", url)
            return None
        t = t.model_dump(by_alias=True, exclude_none=True)
        return t
