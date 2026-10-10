# Xmodmap Configuration (`config/xmodmap/`)

This directory contains custom X11 key modifier and keycode correction maps.

## Files & Purposes

- **`Xmodmap`**:
  Defines critical keyboard corrections for Barrier KVM clients and AZERTY keyboards:
  - Maps dedicated keycode 197 to `Arabic_jeem` across all layout groups so Barrier resolves the Arabic letter `ج` cleanly without touching keycode 18 (digit 9).
  - Maps dedicated keycode 202 to `Arabic_thal` across all layout groups so Barrier resolves `ذ` cleanly without touching keycode 51 (`\`).
  - Restores keycode 18 (`ç` / `9`) and keycode 51 (`*` / `µ` / `\`) to clean standard behavior.
