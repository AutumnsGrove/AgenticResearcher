"""
Implementation Verification Script

This script verifies that the provider abstraction layer has been correctly implemented.
It checks that all required methods are present and that the structure matches the specification.
"""

import sys
from pathlib import Path

def verify_base_provider():
    """Verify BaseProvider has all required abstract methods."""
    print("Checking BaseProvider (providers/base.py)...")
    
    required_methods = [
        "create_agent",
        "send_message",
        "call_tool",
        "get_token_count",
        "get_cost"
    ]
    
    required_properties = [
        "big_model_name",
        "small_model_name",
        "provider_name"
    ]
    
    base_file = Path("providers/base.py")
    if not base_file.exists():
        print("  ✗ base.py not found!")
        return False
    
    content = base_file.read_text()
    
    # Check methods
    for method in required_methods:
        if f"def {method}" in content:
            print(f"  ✓ {method}() defined")
        else:
            print(f"  ✗ {method}() missing!")
            return False
    
    # Check properties
    for prop in required_properties:
        if f"def {prop}" in content:
            print(f"  ✓ {prop} property defined")
        else:
            print(f"  ✗ {prop} property missing!")
            return False
    
    print("  ✓ BaseProvider complete!\n")
    return True


def verify_claude_provider():
    """Verify ClaudeProvider implements all BaseProvider methods."""
    print("Checking ClaudeProvider (providers/claude_provider.py)...")
    
    required_methods = [
        "create_agent",
        "send_message",
        "call_tool",
        "get_token_count",
        "get_cost"
    ]
    
    required_properties = [
        "big_model_name",
        "small_model_name",
        "provider_name"
    ]
    
    claude_file = Path("providers/claude_provider.py")
    if not claude_file.exists():
        print("  ✗ claude_provider.py not found!")
        return False
    
    content = claude_file.read_text()
    
    # Check class definition
    if "class ClaudeProvider(BaseProvider):" not in content:
        print("  ✗ ClaudeProvider doesn't inherit from BaseProvider!")
        return False
    print("  ✓ Inherits from BaseProvider")
    
    # Check model constants
    if 'BIG_MODEL = "claude-sonnet-4-20250514"' in content:
        print("  ✓ Big model: claude-sonnet-4-20250514")
    else:
        print("  ✗ Big model constant incorrect!")
        return False
    
    if 'SMALL_MODEL = "claude-haiku-3-5-20250307"' in content:
        print("  ✓ Small model: claude-haiku-3-5-20250307")
    else:
        print("  ✗ Small model constant incorrect!")
        return False
    
    # Check methods
    for method in required_methods:
        if f"def {method}" in content:
            print(f"  ✓ {method}() implemented")
        else:
            print(f"  ✗ {method}() missing!")
            return False
    
    # Check properties
    for prop in required_properties:
        if f"def {prop}" in content:
            print(f"  ✓ {prop} property implemented")
        else:
            print(f"  ✗ {prop} property missing!")
            return False
    
    # Check pricing
    if "PRICING" in content:
        print("  ✓ Pricing information included")
    else:
        print("  ✗ Pricing information missing!")
        return False
    
    print("  ✓ ClaudeProvider complete!\n")
    return True


def verify_config_loader():
    """Verify ConfigLoader has all required methods."""
    print("Checking ConfigLoader (utils/config_loader.py)...")
    
    required_methods = [
        "get_provider_key",
        "get_mcp_key",
        "get_limit"
    ]
    
    config_file = Path("utils/config_loader.py")
    if not config_file.exists():
        print("  ✗ config_loader.py not found!")
        return False
    
    content = config_file.read_text()
    
    # Check class definition
    if "class ConfigLoader:" not in content:
        print("  ✗ ConfigLoader class not defined!")
        return False
    print("  ✓ ConfigLoader class defined")
    
    # Check methods
    for method in required_methods:
        if f"def {method}" in content:
            print(f"  ✓ {method}() implemented")
        else:
            print(f"  ✗ {method}() missing!")
            return False
    
    print("  ✓ ConfigLoader complete!\n")
    return True


def verify_logging_config():
    """Verify logging configuration module."""
    print("Checking Logging Config (utils/logging_config.py)...")
    
    logging_file = Path("utils/logging_config.py")
    if not logging_file.exists():
        print("  ✗ logging_config.py not found!")
        return False
    
    content = logging_file.read_text()
    
    # Check for key functions
    if "def setup_logging" in content:
        print("  ✓ setup_logging() defined")
    else:
        print("  ✗ setup_logging() missing!")
        return False
    
    if "def get_logger" in content:
        print("  ✓ get_logger() defined")
    else:
        print("  ✗ get_logger() missing!")
        return False
    
    # Check for timestamp formatting
    if "asctime" in content:
        print("  ✓ Timestamp formatting included")
    else:
        print("  ✗ Timestamp formatting missing!")
        return False
    
    print("  ✓ Logging config complete!\n")
    return True


def verify_secrets_template():
    """Verify secrets.template.json exists and has correct structure."""
    print("Checking secrets template (config/secrets.template.json)...")
    
    template_file = Path("config/secrets.template.json")
    if not template_file.exists():
        print("  ✗ secrets.template.json not found!")
        return False
    
    try:
        import json
        with open(template_file) as f:
            data = json.load(f)
        
        # Check required sections
        if "providers" not in data:
            print("  ✗ 'providers' section missing!")
            return False
        print("  ✓ 'providers' section present")
        
        if "mcp_tools" not in data:
            print("  ✗ 'mcp_tools' section missing!")
            return False
        print("  ✓ 'mcp_tools' section present")
        
        if "limits" not in data:
            print("  ✗ 'limits' section missing!")
            return False
        print("  ✓ 'limits' section present")
        
        # Check providers
        required_providers = ["claude", "openai", "openrouter", "gemini"]
        for provider in required_providers:
            if provider in data["providers"]:
                print(f"  ✓ {provider} provider configured")
            else:
                print(f"  ✗ {provider} provider missing!")
                return False
        
        print("  ✓ secrets template complete!\n")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ✗ Invalid JSON: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("Provider Abstraction Layer - Implementation Verification")
    print("=" * 70)
    print()
    
    results = {
        "BaseProvider": verify_base_provider(),
        "ClaudeProvider": verify_claude_provider(),
        "ConfigLoader": verify_config_loader(),
        "Logging Config": verify_logging_config(),
        "Secrets Template": verify_secrets_template()
    }
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for component, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{component:.<50} {status}")
    
    print()
    
    if all(results.values()):
        print("✓ All checks passed! Implementation is complete.")
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
