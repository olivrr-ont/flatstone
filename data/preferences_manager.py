# data/preferences_manager.py
import json
import os
from typing import Dict, Any
from PyQt6.QtGui import QColor


class PreferencesManager:
    def __init__(self):
        self.preferences_file = os.path.join(os.path.dirname(__file__), "preferences.json")
        self.preferences = self.load_preferences()
        self.workspace = None

    def get_default_preferences(self) -> Dict[str, Any]:
        """Return default preference values"""
        return {
            "grid": {
                "size": 32,
                "color": "#1e1e1e",
                "visible": True
            },
            "background": {
                "color": "#000000"
            },
            "simulation": {
                "tick_rate": 20,
                "auto_start": False,
                "update_delay": 50
            }
        }

    def load_preferences(self) -> Dict[str, Any]:
        """Load preferences from JSON file, use defaults if file doesn't exist or is invalid"""
        defaults = self.get_default_preferences()

        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle missing keys
                    return self._merge_preferences(defaults, loaded)
            else:
                # Create default preferences file
                self.save_preferences_to_file(defaults)
                return defaults
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or unreadable, use defaults
            self.save_preferences_to_file(defaults)
            return defaults

    def _merge_preferences(self, defaults: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded preferences with defaults to handle missing keys"""
        result = defaults.copy()
        for category, values in loaded.items():
            if category in result:
                if isinstance(values, dict) and isinstance(result[category], dict):
                    result[category].update(values)
                else:
                    result[category] = values
            else:
                result[category] = values
        return result

    def save_preferences_to_file(self, preferences: Dict[str, Any] = None) -> None:
        """Save preferences to JSON file"""
        if preferences is None:
            preferences = self.preferences

        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
        except IOError:
            pass  # Silently fail if unable to save

    def save_preferences(self) -> None:
        """Save current preferences to file"""
        self.save_preferences_to_file()

    def get_setting(self, category: str, key: str) -> Any:
        """Get a specific setting value"""
        return self.preferences.get(category, {}).get(key)

    def set_setting(self, category: str, key: str, value: Any) -> None:
        """Set a specific setting value"""
        if category not in self.preferences:
            self.preferences[category] = {}
        self.preferences[category][key] = value
        self.save_preferences()
        self.apply_to_workspace()

    def apply_to_workspace(self) -> None:
        """Apply current preferences to the workspace"""
        if self.workspace is None:
            return

        # Apply grid settings
        grid_size = self.get_setting("grid", "size")
        grid_color = self.get_setting("grid", "color")
        grid_visible = self.get_setting("grid", "visible")

        if grid_size is not None:
            self.workspace.set_grid_size(grid_size)
        if grid_color is not None:
            self.workspace.set_grid_color(QColor(grid_color))
        if grid_visible is not None:
            self.workspace.set_grid_visible(grid_visible)

        # Apply background settings
        bg_color = self.get_setting("background", "color")
        if bg_color is not None:
            self.workspace.set_background_color(QColor(bg_color))

    def reset_to_defaults(self) -> None:
        """Reset all preferences to default values"""
        self.preferences = self.get_default_preferences()
        self.save_preferences()
        self.apply_to_workspace()

    def set_workspace(self, workspace) -> None:
        """Set the workspace instance to apply preferences to"""
        self.workspace = workspace
        # Apply current preferences when workspace is set
        self.apply_to_workspace()