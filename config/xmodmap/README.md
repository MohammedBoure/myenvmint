# Xmodmap Configuration (`config/xmodmap/`)

This directory contains custom X11 key modifier and keycode correction maps.

## Files & Purposes

- **`Xmodmap`**:
  Defines critical keyboard corrections for Barrier KVM clients and AZERTY keyboards:
  - Maps keycode 18 in Arabic mode (Group 2) to `Arabic_jeem` (`ج`), resolving the issue where typing `ج` through Barrier produced `9` or `٩`. French mode remains standard (`ç` / `9`).
  - Maps keycode 51 in Arabic mode (Group 2) to `Arabic_thal` (`ذ`), resolving the issue where typing `ذ` through Barrier produced `\`. French mode remains standard (`*` / `µ`).
  - Cleans keycodes 16 and 19 to provide unique 1-to-1 keysym mappings, preventing duplicate grab collisions in `sxhkd` for top-row number keys across French and Arabic layouts.
  - Normalizes Numpad keycodes (79..90) to `KP_1` through `KP_0` across all levels, guaranteeing consistent workspace switching and window transfers with and without NumLock/Shift.
  - Maps dedicated keycodes 197 and 202 as fallback for direct keysym injection.

