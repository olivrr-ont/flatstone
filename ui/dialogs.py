# ui/dialogs.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                            QWidget, QFormLayout, QSpinBox, QPushButton,
                            QCheckBox, QLabel, QDialogButtonBox, QColorDialog)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class PreferencesDialog(QDialog):
    def __init__(self, preferences_manager, parent=None):
        super().__init__(parent)
        self.preferences_manager = preferences_manager
        self.setWindowTitle("Preferences")
        self.setMinimumSize(400, 300)
        self.setModal(True)

        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create tabs
        self.grid_tab = self.create_grid_tab()
        self.background_tab = self.create_background_tab()
        self.simulation_tab = self.create_simulation_tab()

        self.tab_widget.addTab(self.grid_tab, "Grid")
        self.tab_widget.addTab(self.background_tab, "Background")
        self.tab_widget.addTab(self.simulation_tab, "Simulation")

        # Create button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply |
            QDialogButtonBox.StandardButton.RestoreDefaults
        )
        layout.addWidget(button_box)

        # Connect buttons
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_settings)
        button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(self.reset_to_defaults)

    def create_grid_tab(self) -> QWidget:
        """Create the grid settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QFormLayout()

        # Grid size
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setRange(8, 128)
        self.grid_size_spin.setValue(32)
        self.grid_size_spin.setSingleStep(1)
        form_layout.addRow("Grid Size:", self.grid_size_spin)

        # Grid color
        self.grid_color_button = QPushButton()
        self.grid_color_button.setText("Choose Color...")
        self.grid_color_button.clicked.connect(self.choose_grid_color)
        self.grid_color = QColor("#1e1e1e")
        self.update_grid_color_button()
        form_layout.addRow("Grid Color:", self.grid_color_button)

        # Show grid checkbox
        self.show_grid_checkbox = QCheckBox()
        self.show_grid_checkbox.setChecked(True)
        form_layout.addRow("Show Grid:", self.show_grid_checkbox)

        layout.addLayout(form_layout)
        layout.addStretch()

        return widget

    def create_background_tab(self) -> QWidget:
        """Create the background settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QFormLayout()

        # Background color
        self.bg_color_button = QPushButton()
        self.bg_color_button.setText("Choose Color...")
        self.bg_color_button.clicked.connect(self.choose_background_color)
        self.bg_color = QColor("#000000")
        self.update_bg_color_button()
        form_layout.addRow("Background Color:", self.bg_color_button)

        layout.addLayout(form_layout)
        layout.addStretch()

        return widget

    def create_simulation_tab(self) -> QWidget:
        """Create the simulation settings tab (placeholder)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QFormLayout()

        # Tick rate (disabled for now)
        self.tick_rate_spin = QSpinBox()
        self.tick_rate_spin.setRange(1, 100)
        self.tick_rate_spin.setValue(20)
        self.tick_rate_spin.setEnabled(False)
        form_layout.addRow("Tick Rate:", self.tick_rate_spin)

        # Auto-start (disabled for now)
        self.auto_start_checkbox = QCheckBox()
        self.auto_start_checkbox.setChecked(False)
        self.auto_start_checkbox.setEnabled(False)
        form_layout.addRow("Auto-start:", self.auto_start_checkbox)

        # Update delay (disabled for now)
        self.update_delay_spin = QSpinBox()
        self.update_delay_spin.setRange(0, 500)
        self.update_delay_spin.setValue(50)
        self.update_delay_spin.setEnabled(False)
        form_layout.addRow("Update Delay:", self.update_delay_spin)

        layout.addLayout(form_layout)

        # Add note label
        note_label = QLabel("Note: Simulation settings are placeholders for future engine implementation.")
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: #666; font-style: italic; margin: 10px;")
        layout.addWidget(note_label)

        layout.addStretch()

        return widget

    def choose_grid_color(self):
        """Open color dialog for grid color"""
        color = QColorDialog.getColor(self.grid_color, self, "Choose Grid Color")
        if color.isValid():
            self.grid_color = color
            self.update_grid_color_button()

    def choose_background_color(self):
        """Open color dialog for background color"""
        color = QColorDialog.getColor(self.bg_color, self, "Choose Background Color")
        if color.isValid():
            self.bg_color = color
            self.update_bg_color_button()

    def update_grid_color_button(self):
        """Update grid color button appearance"""
        self.grid_color_button.setStyleSheet(
            f"background-color: {self.grid_color.name()}; color: white;"
            f"border: 1px solid #666; padding: 5px;"
        )

    def update_bg_color_button(self):
        """Update background color button appearance"""
        self.bg_color_button.setStyleSheet(
            f"background-color: {self.bg_color.name()}; color: white;"
            f"border: 1px solid #666; padding: 5px;"
        )

    def load_current_settings(self):
        """Load current settings from preferences manager"""
        # Grid settings
        grid_size = self.preferences_manager.get_setting("grid", "size")
        if grid_size is not None:
            self.grid_size_spin.setValue(grid_size)

        grid_color = self.preferences_manager.get_setting("grid", "color")
        if grid_color is not None:
            self.grid_color = QColor(grid_color)
            self.update_grid_color_button()

        grid_visible = self.preferences_manager.get_setting("grid", "visible")
        if grid_visible is not None:
            self.show_grid_checkbox.setChecked(grid_visible)

        # Background settings
        bg_color = self.preferences_manager.get_setting("background", "color")
        if bg_color is not None:
            self.bg_color = QColor(bg_color)
            self.update_bg_color_button()

        # Simulation settings
        tick_rate = self.preferences_manager.get_setting("simulation", "tick_rate")
        if tick_rate is not None:
            self.tick_rate_spin.setValue(tick_rate)

        auto_start = self.preferences_manager.get_setting("simulation", "auto_start")
        if auto_start is not None:
            self.auto_start_checkbox.setChecked(auto_start)

        update_delay = self.preferences_manager.get_setting("simulation", "update_delay")
        if update_delay is not None:
            self.update_delay_spin.setValue(update_delay)

    def apply_settings(self):
        """Apply current settings from UI to preferences manager"""
        # Grid settings
        self.preferences_manager.set_setting("grid", "size", self.grid_size_spin.value())
        self.preferences_manager.set_setting("grid", "color", self.grid_color.name())
        self.preferences_manager.set_setting("grid", "visible", self.show_grid_checkbox.isChecked())

        # Background settings
        self.preferences_manager.set_setting("background", "color", self.bg_color.name())

        # Simulation settings
        self.preferences_manager.set_setting("simulation", "tick_rate", self.tick_rate_spin.value())
        self.preferences_manager.set_setting("simulation", "auto_start", self.auto_start_checkbox.isChecked())
        self.preferences_manager.set_setting("simulation", "update_delay", self.update_delay_spin.value())

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        # Reset preferences
        self.preferences_manager.reset_to_defaults()

        # Reload UI with default values
        self.load_current_settings()

    def accept(self):
        """Handle OK button click"""
        self.apply_settings()
        super().accept()