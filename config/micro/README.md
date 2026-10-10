# Micro Editor Configuration (`config/micro/`)

This directory contains configuration files, keybindings, and productivity plugins for the Micro terminal text editor.

## Files & Purposes

- **`bindings.json`**:
  Custom keybinding mappings for Micro:
  - `Ctrl-b`: Toggles the file manager tree sidebar (`tree` command).
  - `Ctrl-p`: Triggers the `fzf` fuzzy file searcher for quick file opening.
  - `CtrlLeft` / `CtrlRight`: Word-by-word cursor navigation.
  - `Ctrl-Backspace`, `Alt-Backspace`, `Ctrl-w`, `Ctrl-h`: Deletes the previous word for rapid terminal text editing.

- **`settings.json`**:
  Optimized terminal & SSH editor settings:
  - `"clipboard": "terminal"`: Uses terminal OSC 52 clipboard sequences, resolving SSH clipboard and staircase pasting issues.
  - `"autoindent": false`, `"keepautoindent": false`: Prevents compound indentation staircasing during external terminal/SSH pastes.
  - `"colorscheme": "monokai"`: High-contrast developer-friendly color theme.
  - `"cursorline": true`, `"ruler": true`, `"scrollbar": true`: Visual navigation cues and line numbering.
  - `"hlsearch": true`, `"incsearch": true`: Incremental and highlighted search matching.
  - `"rmtrailingws": true`: Automatically strips trailing whitespace on save.
  - `"saveundo": true`: Preserves undo history across editor sessions.
  - `"softwrap": true`: Wraps long lines smoothly without modifying file contents.
  - `"tabsize": 4`, `"tabstospaces": true`: 4-space indentation standard.
  - `"statusformatl"`: Informative status line displaying file name, modification status, cursor coordinates, filetype, and encoding.
  - `"autoclose": true`: Automatically closes braces and quotes.
  - `"filemanager-openonstart": false`: Keeps editor uncluttered on initial file open.
  - `"openbftype": "tab"`: Avoids multi-pane split views on file picks; opens files directly into active buffer (or new tab if buffer is populated).

- **`plug/`**:
  Directory containing productivity plugins (`filemanager`, `editorconfig`, `fzf`, `bookmark`, `snippets`).
