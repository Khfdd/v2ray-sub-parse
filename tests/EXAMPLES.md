"""
Examples of how to run and work with v2ray-sub-parse tests
"""

# ============================================================================
# BASIC USAGE
# ============================================================================

# Run all tests
# $ pytest tests/

# Run with verbose output
# $ pytest tests/ -v

# Run specific test file
# $ pytest tests/parsers/protocols/test_vless.py

# Run specific test class
# $ pytest tests/parsers/protocols/test_vless.py::TestVLESSParser

# Run specific test method
# $ pytest tests/parsers/protocols/test_vless.py::TestVLESSParser::test_valid_urls_parse_successfully

# ============================================================================
# ADVANCED USAGE
# ============================================================================

# Run with coverage report (terminal)
# $ pytest tests/ --cov=src --cov-report=term

# Run with coverage report (HTML)
# $ pytest tests/ --cov=src --cov-report=html
# Then open htmlcov/index.html in browser

# Run tests matching pattern
# $ pytest tests/ -k "vless"
# $ pytest tests/ -k "tag"

# Run with failure output
# $ pytest tests/ -v --tb=short

# Stop on first failure
# $ pytest tests/ -x

# Show print statements
# $ pytest tests/ -s

# Run specific number of failed tests before stopping
# $ pytest tests/ --maxfail=2

# ============================================================================
# CREATING TESTS FOR NEW PROTOCOL (VMESS EXAMPLE)
# ============================================================================

# Step 1: Create the test file by copying template
# $ cp tests/parsers/protocols/test_template.py tests/parsers/protocols/test_vmess.py

# Step 2: Edit test_vmess.py
# Replace:
#   - <PROTOCOL> with VMESS
#   - <protocol> with vmess
#   - parse_<protocol> with parse_vmess
#   - valid_urls with VMESS URLs
#   - invalid_urls with invalid VMESS URLs
#   - get_test_cases() with VMESS-specific tests

# Example test_vmess.py content:
"""
from src.parsers.protocols.vmess import parse_vmess
from tests.parsers.protocols.base_test import BaseProtocolParserTest

class TestVMESSParser(BaseProtocolParserTest):
    @staticmethod
    def parser(url: str):
        return parse_vmess(url)
    
    valid_urls = [
        "vmess://uuid@host:port",
        "vmess://uuid@host:port?security=tls",
    ]
    
    invalid_urls = [
        "http://uuid@host:port",
        "",
    ]
    
    def get_test_cases(self):
        return [
            {
                'url': "vmess://test-uuid@example.com:443",
                'description': 'Basic VMESS URL',
                'assertions': lambda result: (
                    self.assertEqual(result.settings.address, "example.com"),
                    self.assertEqual(result.settings.port, 443),
                )
            },
        ]
"""

# Step 3: Run tests for new protocol
# $ pytest tests/parsers/protocols/test_vmess.py -v

# ============================================================================
# COMMON TEST PATTERNS
# ============================================================================

# Test 1: Testing URL component parsing
# Use test_url_components() helper method with tuples:
# (url, expected_host, expected_port, expected_uuid)

# Test 2: Testing parameter extraction
# Create URL with parameter and assert extracted value:
# url = "protocol://uuid@host:port?param=value"
# result = self.parser(url)
# self.assertEqual(result.settings.param, "value")

# Test 3: Testing nested objects
# result = self.parser("protocol://uuid@host:port?security=tls")
# self.assertIsNotNone(result.stream_settings.tls_settings)
# self.assertEqual(result.stream_settings.security, "tls")

# Test 4: Testing optional parameters with defaults
# url_with_param = "protocol://uuid@host:port?level=5"
# result_with = self.parser(url_with_param)
# self.assertEqual(result_with.settings.level, 5)
# 
# url_without = "protocol://uuid@host:port"
# result_without = self.parser(url_without)
# self.assertEqual(result_without.settings.level, None)  # or default value

# ============================================================================
# DEBUGGING TESTS
# ============================================================================

# Run single test with output
# $ pytest tests/parsers/protocols/test_vless.py::TestVLESSParser::test_tag_extraction -vvs

# Run with pdb debugger
# Add breakpoint() in test code, then:
# $ pytest tests/parsers/protocols/test_vless.py -s

# Show test names without running
# $ pytest tests/ --collect-only

# Run tests with markers
# $ pytest tests/ -m "not slow"  # if markers are defined

# ============================================================================
# CONTINUOUS INTEGRATION
# ============================================================================

# Typical CI/CD pytest command:
# $ pytest tests/ --cov=src --cov-report=xml --cov-report=html -v --tb=short

# Generate JUnit XML report for CI systems
# $ pytest tests/ --junit-xml=test-results.xml

# ============================================================================
# USEFUL FILES
# ============================================================================

# tests/
#   ├── conftest.py                      # Pytest configuration
#   ├── parsers/
#   │   └── protocols/
#   │       ├── base_test.py             # Base class
#   │       ├── test_vless.py            # VLESS tests
#   │       ├── test_template.py         # Template for new protocols
#   │       └── conftest.py              # Protocol tests config
#   └── README.md                        # Full documentation

# Key files to understand:
# - base_test.py: Contains BaseProtocolParserTest with common functionality
# - test_vless.py: Example of complete protocol tests
# - test_template.py: Template to copy for new protocol tests
# - README.md: Comprehensive documentation
