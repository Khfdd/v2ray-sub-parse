# v2ray-sub-parse

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python library for parsing subscription links and URLs from proxy servers (VLESS, VMESS, Trojan, Shadowsocks, etc.) into structured Python objects using Pydantic models.

## Features

- 🔗 **Subscription Link Parsing**: Parse proxy server URLs into structured Outbound configurations
- 🔌 **Protocol Support**: Built-in support for VLESS with extensible architecture for additional protocols:
  - VLESS (✅ Implemented)
  - VMESS (🔄 Planned)
  - Trojan (🔄 Planned)
  - Shadowsocks (🔄 Planned)
  - And more...

- 📦 **Type-Safe**: Full Pydantic v2 support with type hints and validation
- 🔄 **JSON Serialization**: Easy conversion to JSON for V2Ray/XRay configurations
- ⚡ **Performance**: Uses `orjson` for fast JSON operations

## Installation

```bash
pip install v2ray-sub-parse
```

## Quick Start

```python
from v2ray_sub_parse.parsers.manager import ParserManager

# Parse a single VLESS URL
url = "vless://uuid@example.com:443?encryption=none&type=ws&host=example.com#MyProxy"
outbound = ParserManager.parse(url)

# Convert to dictionary (suitable for V2Ray/XRay config)
if outbound:
    config_dict = outbound.model_dump(by_alias=True, exclude_none=True)
    print(config_dict)

# Parse URL and get dictionary directly
config = ParserManager.parse_as_dict(url)
```

## Supported Protocols

### VLESS (Vision Routing Exception List for Security)

VLESS is a non-stateful protocol that focuses on performance and security. 

Example VLESS URL:
```
vless://uuid@ip:port?encryption=none&type=tcp#ProxyName
vless://uuid@ip:port?encryption=none&type=ws&host=example.com&path=/ws#ProxyName
vless://uuid@ip:port?encryption=none&type=h2#ProxyName
```

## Planned Protocols

- **VMESS**: Message-based protocol with perfect forward secrecy
- **Trojan**: Lightweight proxy protocol that mimics HTTP
- **Shadowsocks**: Stream cipher-based protocol
- More protocols and parsers will be added in future releases

## Architecture

### Core Components

```
src/v2ray_sub_parse/
├── core/
│   ├── base.py              # Pydantic BaseModel configuration
│   ├── outbounds.py         # Outbound and related models
│   ├── stream_settings.py    # Stream transport settings
│   ├── protocols/           # Protocol-specific configurations
│   └── transports/          # Transport protocol definitions
├── parsers/
│   ├── manager.py           # Main parser orchestrator
│   └── protocols/
│       └── vless.py         # VLESS protocol parser
└── __init__.py
```

### ParserManager

The main entry point for parsing subscription links. It:
1. Extracts the protocol scheme from the URL
2. Routes to the appropriate protocol parser
3. Returns a structured `OutboundObject` or None on failure

## Related Projects

This library is designed to work with:

- **[XRay Core](https://github.com/XTLS/Xray-core)** - Enhanced version of V2Ray with better performance and security
- **[V2Ray Core](https://github.com/v2fly/v2ray-core)** - A platform for building proxies

These are the reference implementations for proxy configurations that this library parses.

## Configuration Models

All models use Pydantic v2 with:
- Strict type validation
- CamelCase JSON serialization for V2Ray/XRay compatibility
- Read-only models (frozen=True)
- Enum-based values for protocol-specific options

## Dependencies

- **pydantic**: Data validation and settings management
- **orjson**: Fast JSON serialization/deserialization

## License

MIT License - This library is provided as-is and can be freely used, modified, and distributed by anyone without any requirement for attribution. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to:
- Report issues
- Submit pull requests with new protocol parsers
- Improve documentation
- Add tests and examples

## Roadmap

- [x] VLESS protocol parsing
- [ ] VMESS protocol parsing
- [ ] Trojan protocol parsing
- [ ] Shadowsocks protocol parsing
- [ ] Additional transport protocols
- [ ] Enhanced error reporting and validation
- [ ] CLI tool for subscription management
- [ ] Performance optimizations

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone <repository-url>
cd v2ray-sub-parse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Acknowledgments

This library is built around the specifications and implementations provided by:
- The [XRay Project](https://github.com/XTLS/Xray-core)
- The [V2Ray Project](https://github.com/v2fly/v2ray-core)
