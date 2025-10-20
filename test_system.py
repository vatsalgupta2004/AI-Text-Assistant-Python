"""
Test Script for AI Text Assistant
==================================
Quick tests to verify functionality without API keys.

Author: Contributed for Hacktoberfest 2025
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import main
        import ai_assistant
        import config
        import chat_history
        import web_ui
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration management"""
    print("\nTesting configuration...")
    try:
        from config import Config
        
        config = Config()
        print(f"  Provider: {config.provider}")
        print(f"  Model: {config.get_model()}")
        print(f"  Temperature: {config.temperature}")
        print(f"  Max Tokens: {config.max_tokens}")
        
        # Test validation
        is_valid, error = config.validate()
        if is_valid:
            print("✓ Configuration is valid")
        else:
            print(f"⚠ Configuration warning: {error}")
            print("  (This is expected if API keys are not set)")
        
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_chat_history():
    """Test chat history management"""
    print("\nTesting chat history...")
    try:
        from chat_history import ChatHistory
        
        history = ChatHistory()
        
        # Add test entries
        history.add_entry("Hello", "Hi there!", mode="chat")
        history.add_entry("How are you?", "I'm doing great!", mode="chat")
        history.add_entry("Summarize this", "Summary: ...", mode="summarize")
        
        # Get history
        entries = history.get_history()
        print(f"  Added {len(entries)} test entries")
        
        # Test statistics
        stats = history.get_statistics()
        print(f"  Statistics: {stats['total_messages']} messages, {len(stats['modes_used'])} modes")
        
        # Test search
        results = history.search_history("hello")
        print(f"  Search found {len(results)} results")
        
        # Test save/load
        test_file = "test_history.json"
        if history.save_to_file(test_file):
            print(f"  ✓ Saved to {test_file}")
            
            # Try loading
            new_history = ChatHistory()
            if new_history.load_from_file(test_file):
                print(f"  ✓ Loaded from {test_file}")
                
                # Clean up
                history_dir = Path("chat_history")
                (history_dir / test_file).unlink(missing_ok=True)
                print("  ✓ Cleaned up test file")
        
        print("✓ Chat history working correctly")
        return True
        
    except Exception as e:
        print(f"✗ Chat history error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_providers():
    """Test AI provider initialization (without actual API calls)"""
    print("\nTesting AI providers...")
    try:
        from ai_assistant import AIAssistant, MockProvider
        from config import Config
        
        # Test with mock provider
        config = Config()
        
        print("  Testing provider initialization...")
        providers_tested = []
        
        for provider in ["openai", "huggingface", "ollama"]:
            try:
                config.provider = provider
                assistant = AIAssistant(config)
                providers_tested.append(provider)
                print(f"  ✓ {provider} provider initialized")
            except ValueError as e:
                print(f"  ⚠ {provider} provider: {e} (expected without API key)")
            except ImportError as e:
                print(f"  ⚠ {provider} provider: Missing package - {e}")
        
        if providers_tested:
            print(f"✓ Tested {len(providers_tested)} provider(s)")
        else:
            print("⚠ No providers could be initialized (install packages and set API keys)")
        
        return True
        
    except Exception as e:
        print(f"✗ Provider test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that required files exist"""
    print("\nTesting file structure...")
    required_files = [
        "main.py",
        "ai_assistant.py",
        "config.py",
        "chat_history.py",
        "web_ui.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "CONTRIBUTING.md",
        "LICENSE"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
            print(f"  ✗ Missing: {file}")
        else:
            print(f"  ✓ Found: {file}")
    
    if missing:
        print(f"⚠ {len(missing)} file(s) missing")
    else:
        print("✓ All required files present")
    
    return len(missing) == 0

def test_dependencies():
    """Test that required dependencies are installed"""
    print("\nTesting dependencies...")
    dependencies = {
        "colorama": "Colored terminal output",
        "python-dotenv": "Environment variable management",  
        "flask": "Web framework",
        "flask-cors": "CORS support",
        "openai": "OpenAI API (optional)",
        "huggingface_hub": "Hugging Face API (optional)",
        "requests": "HTTP library"
    }
    
    installed = []
    missing = []
    
    for package, description in dependencies.items():
        try:
            # Try importing with underscore variant
            import_name = package.replace("-", "_")
            __import__(import_name)
            installed.append(package)
            print(f"  ✓ {package}: {description}")
        except ImportError:
            missing.append(package)
            optional = "(optional)" in description
            symbol = "⚠" if optional else "✗"
            print(f"  {symbol} {package}: {description} - NOT INSTALLED")
    
    print(f"\n  Installed: {len(installed)}/{len(dependencies)}")
    
    if missing:
        print(f"\n  To install missing packages:")
        print(f"  pip install {' '.join(missing)}")
    
    return len([m for m in missing if "optional" not in dependencies[m]]) == 0

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("AI Text Assistant - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Chat History", test_chat_history),
        ("AI Providers", test_ai_providers),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys to .env")
        print("3. Run: python main.py")
    else:
        print("\n⚠ Some tests failed. Please fix issues before running.")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
