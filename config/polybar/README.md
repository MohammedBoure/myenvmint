# Polybar Configuration (`config/polybar/`)

This directory houses the Polybar status bar configuration and helper scripts.

## Files & Purposes

- **`config.ini`**:
  The primary Polybar configuration file. Defines:
  - Visual layout: floating dark translucent bar with rounded corners.
  - Workspaces module displaying workspaces 1 through 10.
  - Exact RAM module displaying actual gigabytes used and total (`%gb_used% / %gb_total%`).
  - Network module with real-time download/upload speed indicators (`↓ %downspeed% ↑ %upspeed%`).
  - Daily traffic consumption module powered by vnstat.
  - CPU, volume, and clock modules.

- **`launch.sh`**:
  A shell script that safely terminates existing instances of Polybar and launches the `main` bar on the active display.

- **`scripts/`**:
  Contains Python scripts for custom modules.
