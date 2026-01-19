"""Template for protocol parser tests - Copy and modify this file for new protocols

This is a template file showing how to create tests for a new protocol parser.
To add tests for a new protocol (e.g., VMESS):

1. Copy this file to test_<protocol>.py (e.g., test_vmess.py)
2. Replace <PROTOCOL> with your protocol name (e.g., VMESS)
3. Replace parse_<protocol> with your parser function
4. Update valid_urls and invalid_urls lists
5. Update get_test_cases() with your protocol-specific test cases
6. Add any additional protocol-specific test methods
"""

from src.parsers.protocols. < protocol > import parse_ < protocol >
from typing import List, Dict, Any
from tests.parsers.protocols.base_test import BaseProtocolParserTest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "tests"))


class Test < PROTOCOL > Parser(BaseProtocolParserTest):
    """Test cases for <PROTOCOL> protocol parser"""

    @staticmethod
    def parser(url: str):
        """Parser function for <PROTOCOL> URLs"""
        return parse_ < protocol > (url)

    # List of valid URLs that should parse successfully
    valid_urls = [
        # Add your valid <PROTOCOL> URLs here
        # "<protocol>://...",
    ]

    # List of invalid URLs that should raise exceptions
    invalid_urls = [
        # Add your invalid URLs here
        # "http://...",  # Wrong scheme
        # "",            # Empty
    ]

    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Define specific test cases for <PROTOCOL> parser"""
        return [
            {
                'url': "<protocol>://example@host:port",
                'description': 'Basic <PROTOCOL> URL',
                'assertions': lambda result: (
                    self.assertIsNotNone(result),
                    # Add your assertions here
                )
            },
            # Add more test cases following this pattern
        ]

    # Add protocol-specific test methods below
    # For example:
    # def test_custom_parameter(self):
    #     """Test custom parameter parsing"""
    #     result = self.parser("<protocol>://...?param=value")
    #     self.assertEqual(result.settings.param, "value")


if __name__ == '__main__':
    import unittest
    unittest.main()
