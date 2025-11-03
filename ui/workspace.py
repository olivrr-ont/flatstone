# ui/workspace.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMenu
from PyQt6.QtGui import QPainter, QColor, QPen, QAction
from PyQt6.QtCore import Qt, QRectF, QPointF


class Workspace(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # === Scene setup ===
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        # === Viewport setup ===
        self.scale_factor = 1.0
        self.grid_size = 32
        self.grid_color = QColor(30, 30, 30)
        self.grid_visible = True
        self.setBackgroundBrush(QColor(0, 0, 0))  # Black background

        # Create an initial area to draw the grid
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)

    # === Zoom ===
    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            zoom_in_factor = 1.1
            zoom_out_factor = 1 / zoom_in_factor

            if event.angleDelta().y() > 0:
                zoom_factor = zoom_in_factor
            else:
                zoom_factor = zoom_out_factor

            self.scale(zoom_factor, zoom_factor)
            self.scale_factor *= zoom_factor
        else:
            super().wheelEvent(event)

    # === Draw the background grid ===
    def drawBackground(self, painter, rect: QRectF):
        super().drawBackground(painter, rect)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        # Only draw grid if it's visible
        if not self.grid_visible:
            return

        pen = QPen(self.grid_color)
        pen.setWidth(1)
        painter.setPen(pen)

        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)

        # Draw grid lines
        lines = []
        x = left
        while x < rect.right():
            lines.append((QPointF(x, rect.top()), QPointF(x, rect.bottom())))
            x += self.grid_size

        y = top
        while y < rect.bottom():
            lines.append((QPointF(rect.left(), y), QPointF(rect.right(), y)))
            y += self.grid_size

        for line in lines:
            painter.drawLine(line[0], line[1])

    # === Preferences methods ===
    def set_grid_size(self, size: int):
        """Set grid size and trigger redraw"""
        self.grid_size = size
        self.update()

    def set_grid_color(self, color: QColor):
        """Set grid color and trigger redraw"""
        self.grid_color = color
        self.update()

    def set_background_color(self, color: QColor):
        """Set background color"""
        self.setBackgroundBrush(color)

    def set_grid_visible(self, visible: bool):
        """Set grid visibility and trigger redraw"""
        self.grid_visible = visible
        self.update()

    # === Right-click context menu ===
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # Import submenu
        import_menu = QMenu("Import", self)
        import_redstone = QAction("Redstone Component", self)
        import_blocks = QAction("Other Block", self)
        import_menu.addAction(import_redstone)
        import_menu.addAction(import_blocks)

        # Edit submenu
        edit_menu = QMenu("Edit", self)
        prefs_action = QAction("Preferences...", self)
        edit_menu.addAction(prefs_action)

        # Add to main menu
        menu.addMenu(import_menu)
        menu.addMenu(edit_menu)
        menu.addSeparator()

        # View submenu
        view_menu = QMenu("View", self)
        toggle_grid = QAction("Toggle Grid", self)
        view_menu.addAction(toggle_grid)
        menu.addMenu(view_menu)

        # Connect preferences action to parent's open_preferences method if available
        parent = self.parent()
        while parent and not hasattr(parent, 'open_preferences'):
            parent = parent.parent()

        if parent and hasattr(parent, 'open_preferences'):
            prefs_action.triggered.connect(parent.open_preferences)
            toggle_grid.triggered.connect(parent.toggle_grid)
        else:
            # Fallback to print if no parent with preferences methods
            import_redstone.triggered.connect(lambda: print("Import Redstone Component"))
            import_blocks.triggered.connect(lambda: print("Import Other Block"))
            prefs_action.triggered.connect(lambda: print("Open Preferences"))
            toggle_grid.triggered.connect(lambda: print("Toggle grid visibility"))

        # Show the menu
        menu.exec(event.globalPos())
