# Polybar Scripts (`config/polybar/scripts/`)

This directory contains custom scripts that generate telemetry data for Polybar modules.

## Files & Purposes

- **`traffic_today.py`**:
  Queries the local `vnstat --json` database for the active default network interface. It extracts today's exact bytes received (rx) and transmitted (tx), formats the cumulative consumption into human-readable units (KiB, MiB, GiB), and prints the formatted string for the Polybar status bar.
