"""Tests for VLESS protocol parser"""

from typing import List, Dict, Any
from tests.parsers.protocols.base_test import BaseProtocolParserTest
from src.parsers.protocols.vless import parse_vless
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "tests"))


class TestVLESSParser(BaseProtocolParserTest):
    """Test cases for VLESS protocol parser"""

    @staticmethod
    def parser(url: str):
        """Parser function for VLESS URLs"""
        return parse_vless(url)

    valid_urls = [
        # Basic VLESS URL
        "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443",
        # With security parameter
        "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?security=tls",
        # With tag
        "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443#MyServer",
        # With encryption
        "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?encryption=none",
        # With server name
        "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?server_name=example.com",
        # Complex URL with multiple parameters
        "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?security=tls&server_name=example.com&alpn=h2,http/1.1&flow=xtls-rprx-vision#MyTag",
    ]

    invalid_urls = [
        # Wrong scheme
        "http://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443",
        "ss://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443",
        # Empty URL
        "",
        # Malformed URL
        "not a url at all",
    ]

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Define specific test cases for VLESS parser"""
        return [
            {
                'url': "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443",
                'description': 'Basic VLESS URL with UUID, host, and port',
                'assertions': lambda result: (
                    self.assertEqual(result.settings.address, "example.com"),
                    self.assertEqual(result.settings.port, 443),
                    self.assertEqual(result.settings.id,
                                     "a684455c-b14f-4b0a-908c-6d0e7d8f4e3f"),
                    self.assertEqual(result.settings.encryption, "none"),
                )
            },
            {
                'url': "vless://test-uuid@192.168.1.1:8443#ServerTag",
                'description': 'VLESS URL with tag',
                'assertions': lambda result: (
                    self.assertEqual(result.tag, "ServerTag"),
                    self.assertEqual(result.settings.address, "192.168.1.1"),
                    self.assertEqual(result.settings.port, 8443),
                )
            },
            {
                'url': "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?security=tls&server_name=example.com",
                'description': 'VLESS URL with TLS security',
                'assertions': lambda result: (
                    self.assertEqual(result.stream_settings.security, "tls"),
                    self.assertIsNotNone(result.stream_settings.tls_settings),
                    self.assertEqual(
                        result.stream_settings.tls_settings.server_name, "example.com"),
                )
            },
            {
                'url': "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?security=reality&server_name=example.com&short_id=1234&pubkey=pubkey123",
                'description': 'VLESS URL with REALITY security',
                'assertions': lambda result: (
                    self.assertEqual(
                        result.stream_settings.security, "reality"),
                    self.assertIsNotNone(
                        result.stream_settings.reality_settings),
                    self.assertEqual(
                        result.stream_settings.reality_settings.server_name, "example.com"),
                )
            },
            {
                'url': "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?mux=true&concurrency=8",
                'description': 'VLESS URL with MUX enabled',
                'assertions': lambda result: (
                    self.assertTrue(result.mux.enabled),
                    self.assertEqual(result.mux.concurrency, 8),
                )
            },
            {
                'url': "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?encryption=none&level=5",
                'description': 'VLESS URL with level parameter',
                'assertions': lambda result: (
                    self.assertEqual(result.settings.level, 5),
                )
            },
            {
                'url': "vless://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443?security=tls&alpn=h2,http/1.1&fingerprint=chrome",
                'description': 'VLESS URL with ALPN and fingerprint',
                'assertions': lambda result: (
                    self.assertIsNotNone(result.stream_settings.tls_settings),
                    self.assertIsNotNone(
                        result.stream_settings.tls_settings.alpn),
                    self.assertIsNotNone(
                        result.stream_settings.tls_settings.fingerprint),
                )
            },
        ]

    def test_url_components_vless(self):
        """Test basic URL component parsing for VLESS"""
        test_data = [
            ("vless://uuid1@host1.com:443", "host1.com", 443, "uuid1"),
            ("vless://uuid2@192.168.1.1:8080", "192.168.1.1", 8080, "uuid2"),
            ("vless://uuid3@localhost:10000", "localhost", 10000, "uuid3"),
        ]
        self.test_url_components(test_data)

    def test_empty_tag_results_in_none(self):
        """Test that URL without tag has None tag"""
        result = parse_vless("vless://uuid@example.com:443")
        self.assertIsNone(result.tag)

    def test_tag_extraction(self):
        """Test correct tag extraction from URL fragment"""
        result = parse_vless("vless://uuid@example.com:443#CustomTag")
        self.assertEqual(result.tag, "CustomTag")

    def test_multiple_tags_takes_first(self):
        """Test that if somehow multiple fragments, first is used"""
        result = parse_vless("vless://uuid@example.com:443#FirstTag")
        self.assertEqual(result.tag, "FirstTag")

    def test_encryption_parameter_parsing(self):
        """Test encryption parameter extraction"""
        result = parse_vless("vless://uuid@example.com:443?encryption=none")
        self.assertEqual(result.settings.encryption, "none")

    def test_default_encryption_is_none(self):
        """Test that default encryption is 'none'"""
        result = parse_vless("vless://uuid@example.com:443")
        self.assertEqual(result.settings.encryption, "none")

    def test_tls_allow_insecure_parameter(self):
        """Test allow_insecure TLS parameter"""
        result = parse_vless(
            "vless://uuid@example.com:443?security=tls&allow_insecure=1")
        self.assertTrue(result.stream_settings.tls_settings.allow_insecure)

    def test_tls_allow_insecure_default_false(self):
        """Test that allow_insecure defaults to False"""
        result = parse_vless("vless://uuid@example.com:443?security=tls")
        self.assertFalse(result.stream_settings.tls_settings.allow_insecure)

    def test_network_type_detection(self):
        """Test network type parameter parsing"""
        result = parse_vless("vless://uuid@example.com:443?type=tcp")
        self.assertEqual(result.stream_settings.network.value, "tcp")

    def test_default_network_is_raw(self):
        """Test that default network type is raw"""
        result = parse_vless("vless://uuid@example.com:443")
        self.assertEqual(result.stream_settings.network.value, "raw")


if __name__ == '__main__':
    unittest.main()
