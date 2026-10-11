# Micro Autocomplete Tooltip (`config/micro/plug/micro-autocomplete-tooltip/`)

Show **interactive suggestions in a tooltip** directly at the cursor location. Works for both active text buffers and the bottom Command bar (`>`). Hit `Tab` to trigger suggestions, and navigate with `Up`/`Down` arrows.

## Files & Purposes

- **`autocomplete_tooltip.lua`**:
  Main plugin entry point. Listens to editor events (`onAnyEvent`), queries active buffer suggestions, constructs the floating tooltip sub-pane, and intercepts `CursorUp` / `CursorDown` when `"autocomplete_tooltip.EnableCursorUpDown": true` to cycle through candidates.
- **`tooltip.lua`**:
  Tooltip module handling geometry calculation, fitting window coordinates around the cursor (`FitAroundLocation`), dynamic resizing, and buffer cleanup.
- **`repo.json`**:
  Plugin package description and repository manifest for Micro plugin manager.
- **`ENABLE_FOR_MICRO.sh`**:
  Shell helper script to create symlinks in `~/.config/micro/plug/`.
- **`colorschemes/`**:
  Dedicated directory containing the tooltip theme palette (`autocomplete-tooltip.micro`).
- **`syntax/`**:
  Dedicated directory containing syntax highlighting definitions for tooltip suggestions (`autocomplete-tooltip.yaml`).
- **`LICENSE`**:
  MIT License document.
