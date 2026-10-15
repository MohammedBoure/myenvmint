# Picom Configuration (`config/picom/`)

This directory contains the Picom X11 compositor configuration.

## Files & Purposes

- **`picom.conf`**:
  The Picom configuration file. Features include:
  - High-performance OpenGL rendering backend (`glx`) with VSync enabled.
  - Window outline / border: applies a crisp 3px accent (`#5294E2`) outline around all application windows for effortless window distinction and separation.
  - Window corner radius set to 4px for modern aesthetics.
  - Inactive window dimming (`inactive-dim = 0.12`) to give immediate visual hierarchy to the focused client.
  - Exclusion rules ensuring Polybar, docks, popups, and desktop backgrounds are not dimmed or outlined.
