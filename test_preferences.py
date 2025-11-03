#!/usr/bin/env python3
"""Test preferences functionality without GUI dependencies"""

import json
import os
import sys

# Add current directory to path
sys.path.insert(0, '.')

class MockQColor:
    """Mock QColor class for testing"""
    def __init__(self, color_string):
        if isinstance(color_string, str):
            self.color = color_string
        else:
            self.color = "#000000"

    def name(self):
        return self.color

# Replace PyQt6 import with mock
sys.modules['PyQt6'] = type(sys)('PyQt6')
sys.modules['PyQt6.QtGui'] = type(sys)('PyQt6.QtGui')
sys.modules['PyQt6.QtGui'].QColor = MockQColor

# Now import our classes
from data.preferences_manager import PreferencesManager

def test_preferences_manager():
    print("Testing PreferencesManager...")

    # Create a test preferences file
    test_file = "/tmp/test_preferences.json"

    # Backup original file path and set test path
    manager = PreferencesManager()
    original_file = manager.preferences_file
    manager.preferences_file = test_file

    try:
        # Test 1: Default preferences
        print("✓ Testing default preferences...")
        defaults = manager.get_default_preferences()
        assert defaults["grid"]["size"] == 32
        assert defaults["grid"]["color"] == "#1e1e1e"
        assert defaults["grid"]["visible"] == True
        assert defaults["background"]["color"] == "#000000"

        # Test 2: Load preferences (should create default file)
        print("✓ Testing preferences loading...")
        prefs = manager.load_preferences()
        assert prefs["grid"]["size"] == 32
        assert prefs["background"]["color"] == "#000000"

        # Test 3: Set and get settings
        print("✓ Testing setting/getting values...")
        manager.set_setting("grid", "size", 64)
        assert manager.get_setting("grid", "size") == 64

        manager.set_setting("background", "color", "#ffffff")
        assert manager.get_setting("background", "color") == "#ffffff"

        # Test 4: File persistence
        print("✓ Testing file persistence...")
        assert os.path.exists(test_file)

        with open(test_file, 'r') as f:
            saved_data = json.load(f)
            assert saved_data["grid"]["size"] == 64
            assert saved_data["background"]["color"] == "#ffffff"

        # Test 5: Reset to defaults
        print("✓ Testing reset to defaults...")
        manager.reset_to_defaults()
        assert manager.get_setting("grid", "size") == 32
        assert manager.get_setting("background", "color") == "#000000"

        print("✅ All PreferencesManager tests passed!")

    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        manager.preferences_file = original_file

def test_file_structure():
    print("\nTesting file structure...")

    # Check if all files exist
    required_files = [
        "data/preferences_manager.py",
        "ui/dialogs.py",
        "ui/workspace.py",
        "ui/main_window.py"
    ]

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False

    # Check if files have content
    for file_path in required_files:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if len(content) > 100:  # Reasonable content length
                print(f"✓ {file_path} has content")
            else:
                print(f"❌ {file_path} appears empty or too short")
                return False

    print("✅ File structure test passed!")
    return True

def test_imports():
    print("\nTesting imports...")

    try:
        # Test preferences manager imports (with mock)
        print("✓ PreferencesManager imports successfully")

        # Test basic functionality
        manager = PreferencesManager()
        defaults = manager.get_default_preferences()
        print("✓ PreferencesManager can create default values")

        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running Preferences Dialog Implementation Tests\n")

    success = True

    # Run tests
    success &= test_file_structure()
    success &= test_imports()
    success &= test_preferences_manager()

    if success:
        print("\n🎉 All tests passed! Implementation appears correct.")
    else:
        print("\n❌ Some tests failed. Please review the implementation.")
        sys.exit(1)