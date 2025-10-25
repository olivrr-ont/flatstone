# Flatstone - 2D Minecraft Redstone Simulator

**Flatstone** is a 2D sandbox tool for designing and experimenting with Minecraft Redstone circuits.  
It allows players and creators to prototype Redstone contraptions in a clean, visual environment without building complex structures in the game itself.

---

## Project Structure
```bash
flatstone/
│
├─ main.py # Entry point for the application
├─ ui/
│ ├─ main_window.py # Main window, menus, status bar
│ ├─ workspace.py # 2D grid canvas, zoom, pan, right-click menu
│ └─ dialogs.py # Preferences and import dialogs
│
├─ engine/
│ ├─ redstone_logic.py # Tick update and simulation logic
│ ├─ components.py # Redstone components (dust, repeater, torch, etc.)
│ └─ world_state.py # Grid data, block positions, and states
│
├─ assets/
│ ├─ textures/ # Minecraft textures for blocks and items
│ └─ icons/ # UI icons
│
└─ data/
├─ preferences.json # User preferences
└─ saves/ # Saved projects
```
## Features (So Far)

- **Main Window**  
  - Menu bar with tabs: `File`, `Edit`, `View`, `Window`, `Help`  
  - Status bar showing current state

- **2D Grid Workspace**  
  - Scrollable and zoomable canvas  
  - Black background with subtle dark grey grid lines  
  - Placeholder for drawing blocks

- **Right-Click Context Menu**  
  - `Import` → Redstone Components / Other Blocks  
  - `Edit` → Preferences…  
  - `View` → Toggle Grid  
  - Currently prints actions to console (stub for future dialogs)

- **Zoom & Pan**  
  - Ctrl + Scroll = Zoom  
  - Middle-click drag = Pan around the workspace

---

## Dependencies

- Python 3.9+  
- [PyQt6](https://pypi.org/project/PyQt6/)

Install dependencies via pip:
```bash
pip install -r requirements.txt
```
## Next Steps / Planned Features

- Implement Import Dialogs to select and place Redstone components and other blocks

- Add Preferences Dialog to adjust grid, background, and simulation settings

- Begin implementing the Redstone simulation engine

- Enable placing blocks on the grid and simulating signals

- Allow saving and loading projects

- Add visualization for signal propagation and tick updates
