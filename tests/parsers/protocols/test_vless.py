"""Tests for VLESS protocol parser"""

import sys
import typing
import unittest
from tests.parsers.protocols.base_test import BaseProtocolParserTest
from src.v2ray_sub_parse.parsers.protocols.vless import parse_vless
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "tests"))


class TestVLESSParser(BaseProtocolParserTest):
    """Test cases for VLESS protocol parser"""

    @staticmethod
    def parser(url: str):
        """Parser function for VLESS URLs"""
        return parse_vless(url).model_dump(by_alias=True, exclude_none=True)

    invalid_urls = [
        "http://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443",
        "ss://a684455c-b14f-4b0a-908c-6d0e7d8f4e3f@example.com:443",
        "",
        "not a url at all",
    ]

    def get_test_cases(self) -> list[dict[str, typing.Any]]:
        """Define specific test cases for VLESS parser"""
        def _vless_raw_reality(result: dict[str, typing.Any]):
            self.assertEqual(
                result, {
                    'protocol': 'vless',
                    'settings':
                        {
                            'vnext':
                            [
                                {'address': 'gmfstt.test.domain',
                                 'port': 443,
                                 'users': [
                                     {
                                         'id': '0f2bcbec-5447-49e1-8ba3-c7078a02bf90',
                                         'encryption': 'none',
                                         'flow': 'none'}
                                 ]
                                 }
                            ]
                        },
                    'tag': '🇩🇪 Германия FAST⚡️| 🟢 VPNHub',
                    'streamSettings': {
                        'network': 'raw',
                            'security': 'reality',
                            'realitySettings':
                            {'fingerprint':
                             'chrome'},
                            'rawSettings': {}
                        }, 'mux': {'enabled': False, 'xudpProxyudp443': 'skip'}}
            )

        def _vless_xhttp_reality(result: dict[str, typing.Any]):
            self.assertEqual(
                result, {
                    'protocol': 'vless',
                    'settings': {
                        'vnext': [
                            {
                                'address': 'gmfstt.test.domain',
                                'port': 8443,
                                'users': [
                                    {
                                        'id': '0f2bcbec-5447-49e1-8ba3-c7078a02bf90',
                                        'encryption': 'none',
                                        'flow': 'none'
                                    }
                                ]
                            }
                        ]
                    },
                    'tag': '%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20FAST%E2%9A%A1%EF%B8%8F%7C%20%F0%9F%9F%A2%20VPNHub',
                    'streamSettings': {
                        'network': 'raw',
                        'security': 'reality',
                        'realitySettings': {'fingerprint': 'chrome'},
                        'rawSettings': {}
                    },
                    'mux': {'enabled': False, 'xudpProxyudp443': 'skip'}}
            )

        return [
            {
                'url': "vless://0f2bcbec-5447-49e1-8ba3-c7078a02bf90@gmfstt.test.domain:443?security=reality&type=tcp&headerType=&path=&host=&sni=www.apple.com&fp=chrome&pbk=EJKcPSl0dv7mtU26gg6tUmKPw_aDvO2AHraRgNn6B14&sid=425ba80cd1a821a8#%F0%9F%87%A9%F0%9F%87%AA%20%D0%93%D0%B5%D1%80%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20FAST%E2%9A%A1%EF%B8%8F%7C%20%F0%9F%9F%A2%20VPNHub",
                'description': 'VLESS-RAW-REALITY',
                'assertions': _vless_raw_reality
            },
            {
                'url': "vless://0f2bcbec-5447-49e1-8ba3-c7078a02bf90@bs.test.domain:8443?security=reality&type=xhttp&headerType=&path=%2Fabout&host=www.apple.com&mode=auto&extra=%7B%22scMaxEachPostBytes%22%3A+1000000%2C+%22scMaxConcurrentPosts%22%3A+100%2C+%22scMinPostsIntervalMs%22%3A+30%2C+%22xPaddingBytes%22%3A+%22100-1000%22%2C+%22noGRPCHeader%22%3A+false%7D&sni=vk.com&fp=chrome&pbk=nxOc44-7o4IOVrNHDuWTZk3eKufjZM-aQa1aHKRc-io&sid=772b7ad61ba0fa12#%D0%9E%D0%B1%D1%85%D0%BE%D0%B4%20%D0%91%D0%A1%20%231%20%5BX%5D%20%7C%20%20%F0%9F%9F%A2%20VPNHub",
                'description': 'VLESS-XHTTP-REALITY',
                'assertions': _vless_xhttp_reality
            }
        ]


if __name__ == '__main__':
    unittest.main()
