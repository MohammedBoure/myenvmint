# Xmodmap Configuration (`config/xmodmap/`)

This directory contains custom X11 key modifier and keycode correction maps.

## Files & Purposes

- **`Xmodmap`**:
  Defines critical keyboard corrections for Barrier KVM clients and AZERTY keyboards:
  - Maps keycode 18 in Arabic mode (Group 2) to `Arabic_jeem` (`ج`), resolving the issue where typing `ج` through Barrier produced `9` or `٩`. French mode remains standard (`ç` / `9`).
  - Maps keycode 51 in Arabic mode (Group 2) to `Arabic_thal` (`ذ`), resolving the issue where typing `ذ` through Barrier produced `\`. French mode remains standard (`*` / `µ`).
  - Maps dedicated keycodes 197 and 202 as fallback for direct keysym injection.
