"""Base test class for protocol parsers - scalable for future protocol tests"""

import sys
from pathlib import Path
import unittest
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "tests"))


class BaseProtocolParserTest(ABC, unittest.TestCase):
    """
    Abstract base class for protocol parser tests.

    Provides a scalable framework for testing different protocol parsers.
    Subclasses should define test cases specific to their protocol.

    Example:
        class VLESSParserTest(BaseProtocolParserTest):
            @staticmethod
            def parser(url):
                return parse_vless(url)

            valid_urls = [...]
            invalid_urls = [...]

            def get_test_cases(self):
                return [...]
    """

    @staticmethod
    @abstractmethod
    def parser(url: str):
        """Parser function to test. Should be overridden by subclass."""
        pass

    valid_urls: List[str] = []
    invalid_urls: List[str] = []

    @abstractmethod
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Return list of test cases for this protocol.

        Each test case should be a dict with:
        - 'url': str - The URL to parse
        - 'description': str - Description of what is being tested
        - 'assertions': callable - Function that takes the parsed result
                                   and makes assertions

        Returns:
            List of test case dicts
        """
        pass

    def test_valid_urls_parse_successfully(self):
        """Test that all valid URLs parse without raising exceptions"""
        for url in self.valid_urls:
            with self.subTest(url=url):
                try:
                    result = self.parser(url)
                    self.assertIsNotNone(result)
                except Exception as e:
                    self.fail(
                        f"Parser raised exception for valid URL: {url}\nError: {e}")

    def test_invalid_urls_raise_exception(self):
        """Test that all invalid URLs raise ValueError"""
        for url in self.invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises((ValueError, Exception)):
                    self.parser(url)

    def test_all_test_cases(self):
        """Run all custom test cases from get_test_cases"""
        test_cases = self.get_test_cases()

        for test_case in test_cases:
            with self.subTest(description=test_case['description']):
                url = test_case['url']
                try:
                    result = self.parser(url)
                    test_case['assertions'](result)
                except Exception as e:
                    self.fail(
                        f"Test case '{test_case['description']}' failed for URL: {url}\n"
                        f"Error: {e}"
                    )

    def test_url_components(self, test_data: List[Tuple[str, str, int, str]]):
        """
        Helper method to test URL components (scheme, host, port, etc)

        Args:
            test_data: List of tuples (url, expected_host, expected_port, expected_uuid)
        """
        for url, expected_host, expected_port, expected_uuid in test_data:
            with self.subTest(url=url):
                result = self.parser(url)
                if result.settings:
                    self.assertEqual(result.settings.address, expected_host)
                    self.assertEqual(result.settings.port, expected_port)
                    self.assertEqual(result.settings.id, expected_uuid)
