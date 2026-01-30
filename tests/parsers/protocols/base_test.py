"""Base test class for protocol parsers - scalable for future protocol tests"""

import sys
import typing
import unittest
from pathlib import Path
from abc import ABC, abstractmethod

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
    def parser(url: str) -> dict[str, typing.Any]:
        """Parser function to test. Should be overridden by subclass."""
        pass

    invalid_urls: list[str] = []

    @abstractmethod
    def get_test_cases(self) -> list[dict[str, typing.Any]]:
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
                except Exception as e:
                    self.fail(
                        f"Parser raised exception for URL: {url}\nError: {e}")
                try:
                    test_case['assertions'](result)
                except Exception as e:
                    self.fail(
                        f"Test case '{test_case['description']}' failed for URL: {url}\n"
                        f"Error: {e}\n"
                        f"Result: {result}\n\n"
                    )
