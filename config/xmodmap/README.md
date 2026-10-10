# Xmodmap Configuration (`config/xmodmap/`)

This directory contains custom X11 key modifier and keycode correction maps.

## Files & Purposes

- **`Xmodmap`**:
  Defines critical keyboard corrections for Barrier KVM clients and AZERTY keyboards:
  - Remaps keycode 18 to `Arabic_jeem` (and `U062C`) in Arabic mode to eliminate the bug where typing `ج` produces `٩`.
  - Remaps keycode 51 to `Arabic_thal` in Arabic mode to eliminate the bug where typing `ذ` produces `\`.
