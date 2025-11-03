# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QStatusBar
from PyQt6.QtGui import QAction
from ui.workspace import Workspace
from ui.dialogs import PreferencesDialog
from data.preferences_manager import PreferencesManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flatstone - Redstone Simulator")
        self.setGeometry(100, 100, 1200, 800)

        # === Central Workspace ===
        self.workspace = Workspace()
        self.setCentralWidget(self.workspace)

        # === Preferences Manager ===
        self.preferences_manager = PreferencesManager()
        self.preferences_manager.set_workspace(self.workspace)

        # === Menus ===
        self.create_menus()

        # === Status Bar ===
        status = QStatusBar()
        status.showMessage("Ready")
        self.setStatusBar(status)

    def create_menus(self):
        menu_bar = self.menuBar()

        # --- File ---
        file_menu = menu_bar.addMenu("File")
        for name in ["New Project", "Open Project", "Save", "Exit"]:
            action = QAction(name, self)
            if name == "Exit":
                action.triggered.connect(self.close)
            file_menu.addAction(action)

        # --- Edit ---
        edit_menu = menu_bar.addMenu("Edit")
        prefs_action = QAction("Preferences...", self)
        edit_menu.addAction(prefs_action)

        # --- View ---
        view_menu = menu_bar.addMenu("View")
        grid_action = QAction("Toggle Grid", self)
        view_menu.addAction(grid_action)

        # --- Window ---
        window_menu = menu_bar.addMenu("Window")
        comp_lib_action = QAction("Component Library", self)
        window_menu.addAction(comp_lib_action)

        # --- Help ---
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About Flatstone", self)
        help_menu.addAction(about_action)
