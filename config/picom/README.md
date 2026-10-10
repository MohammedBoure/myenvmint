# Picom Configuration (`config/picom/`)

This directory contains the Picom X11 compositor configuration.

## Files & Purposes

- **`picom.conf`**:
  The Picom configuration file. Features include:
  - High-performance OpenGL rendering backend (`glx`) with VSync enabled.
  - Active window focus highlight: applies a crisp 2px white (`#FFFFFF`) outline/border around the currently focused window.
  - Window corner radius set to 4px for modern aesthetics.
  - Inactive window dimming (`inactive-dim = 0.10`) to give immediate visual hierarchy to the focused client.
  - Exclusion rules ensuring Polybar, docks, popups, and desktop backgrounds are not dimmed or outlined.
