# Tests for v2ray-sub-parse

This directory contains tests for the v2ray-sub-parse project, organized in a scalable structure to easily add tests for new protocols and parsers.

## Structure

```
tests/
├── parsers/
│   └── protocols/
│       ├── base_test.py          # Base class for all protocol parser tests
│       ├── test_vless.py         # Tests for VLESS protocol
│       ├── test_vmess.py         # (Future) Tests for VMESS protocol
│       ├── test_ss.py            # (Future) Tests for Shadowsocks protocol
│       ├── test_template.py      # Template for new protocol tests
│       └── ...
├── conftest.py                   # Pytest configuration
└── README.md                      # This file
```

## Quick Start

### Run all tests
```bash
source venv/bin/activate  # if using virtual environment
pytest tests/
```

### Run tests for specific protocol
```bash
pytest tests/parsers/protocols/test_vless.py -v
```

### Run with coverage report
```bash
pytest tests/ --cov=src --cov-report=html
pytest tests/ --cov=src --cov-report=term
```

### Run specific test
```bash
pytest tests/parsers/protocols/test_vless.py::TestVLESSParser::test_valid_urls_parse_successfully -v
```

## Test Structure

### Base Class: `BaseProtocolParserTest`

All protocol parser tests inherit from `BaseProtocolParserTest` which provides:

#### Automatic Tests (inherited from base class)
- `test_valid_urls_parse_successfully()` - Tests that all valid URLs in `valid_urls` parse without errors
- `test_invalid_urls_raise_exception()` - Tests that all URLs in `invalid_urls` raise exceptions
- `test_all_test_cases()` - Runs all custom test cases from `get_test_cases()`

#### Helper Methods
- `test_url_components()` - Tests URL component parsing (host, port, UUID, etc.)

#### Test Case Format

Each test case in `get_test_cases()` is a dictionary with:

```python
{
    'url': 'the://url:to/test',
    'description': 'What this test case validates',
    'assertions': lambda result: (
        self.assertEqual(result.attribute, expected_value),
        self.assertIsNotNone(result.other_attribute),
        # ... more assertions
    )
}
```

## Adding Tests for a New Protocol

### Step 1: Create Test File

Copy the template file and rename it:

```bash
cp tests/parsers/protocols/test_template.py tests/parsers/protocols/test_<protocol>.py
```

### Step 2: Implement Test Class

```python
from src.parsers.protocols.vmess import parse_vmess
from base_test import BaseProtocolParserTest

class TestVMESSParser(BaseProtocolParserTest):
    @staticmethod
    def parser(url: str):
        return parse_vmess(url)
    
    valid_urls = [
        "vmess://uuid@host:port",
        "vmess://uuid@host:port?param=value",
    ]
    
    invalid_urls = [
        "http://uuid@host:port",  # Wrong scheme
        "",  # Empty
    ]
    
    def get_test_cases(self):
        return [
            {
                'url': "vmess://test-uuid@example.com:443",
                'description': 'Basic VMESS URL parsing',
                'assertions': lambda result: (
                    self.assertEqual(result.settings.address, "example.com"),
                    self.assertEqual(result.settings.port, 443),
                    self.assertEqual(result.settings.id, "test-uuid"),
                )
            },
            # Add more test cases
        ]
    
    # Add protocol-specific tests
    def test_custom_feature(self):
        """Test protocol-specific feature"""
        result = self.parser("vmess://uuid@host:port?custom=value")
        self.assertEqual(result.settings.custom, "value")
```

### Step 3: Run Tests

```bash
pytest tests/parsers/protocols/test_<protocol>.py -v
```

## Example: VLESS Parser Tests

The VLESS parser tests (`test_vless.py`) demonstrate the full structure:

1. **Valid URLs Test** - Ensures known good URLs parse successfully
2. **Invalid URLs Test** - Ensures invalid URLs raise exceptions
3. **Custom Test Cases** - Specific parsing scenarios with assertions
4. **URL Component Tests** - Tests extraction of URL parts (host, port, UUID)
5. **Parameter Tests** - Tests specific protocol parameters (encryption, security, etc.)

## Best Practices

### 1. Test Organization
- Keep related test cases together
- Use descriptive names for test methods
- Group similar assertions in test cases

### 2. URL Examples
- Include basic URLs with minimal parameters
- Include complex URLs with multiple parameters
- Include edge cases (empty parameters, special characters, etc.)

### 3. Assertions
- Use `subTest()` for parametrized tests to show which case failed
- Include helpful error messages
- Test both positive cases (should work) and negative cases (should fail)

### 4. Coverage
- Test basic URL structure parsing
- Test optional parameters and defaults
- Test parameter validation
- Test error handling for invalid inputs

### 5. Maintainability
- Keep tests simple and focused
- Use helper methods for common patterns
- Document non-obvious test cases
- Update tests when parser behavior changes

## Example Test Methods

### Testing URL Components
```python
def test_url_components_vless(self):
    """Test basic URL component parsing"""
    test_data = [
        ("vless://uuid1@host1.com:443", "host1.com", 443, "uuid1"),
        ("vless://uuid2@192.168.1.1:8080", "192.168.1.1", 8080, "uuid2"),
    ]
    self.test_url_components(test_data)
```

### Testing Optional Parameters
```python
def test_encryption_parameter(self):
    """Test encryption parameter parsing"""
    result = self.parser("vless://uuid@example.com:443?encryption=none")
    self.assertEqual(result.settings.encryption, "none")

def test_default_encryption(self):
    """Test that encryption defaults to 'none'"""
    result = self.parser("vless://uuid@example.com:443")
    self.assertEqual(result.settings.encryption, "none")
```

### Testing Complex Parameters
```python
def test_tls_configuration(self):
    """Test TLS configuration parsing"""
    url = "vless://uuid@example.com:443?security=tls&server_name=example.com&allow_insecure=1"
    result = self.parser(url)
    
    self.assertEqual(result.stream_settings.security, "tls")
    self.assertIsNotNone(result.stream_settings.tls_settings)
    self.assertEqual(result.stream_settings.tls_settings.server_name, "example.com")
    self.assertTrue(result.stream_settings.tls_settings.allow_insecure)
```

## Troubleshooting

### Test Discovery Issues
If pytest doesn't find your tests:
- Ensure file is named `test_*.py` or `*_test.py`
- Ensure class is named `Test*` 
- Ensure methods are named `test_*`
- Check that `conftest.py` is in the tests directory

### Import Errors
If you get import errors:
- Check that `src/__init__.py` exists
- Verify relative imports match the package structure
- Make sure virtual environment is activated if using one

### Parser Not Found
If the parser function can't be imported:
- Verify the parser file exists in `src/parsers/protocols/`
- Check that the function name matches (e.g., `parse_vless`)
- Ensure the parser is implemented in the module

## Contributing

When adding tests for a new protocol:
1. Follow the same structure as existing protocol tests
2. Use the base class for common functionality
3. Add comprehensive test cases covering main features
4. Test both success and failure paths
5. Document any non-obvious test scenarios
6. Ensure all tests pass before committing

