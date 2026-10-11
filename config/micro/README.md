# Micro Editor Configuration (`config/micro/`)

This directory contains configuration files, keybindings, and productivity plugins for the Micro terminal text editor.

## Files & Purposes

- **`bindings.json`**:
  Custom keybinding mappings for Micro:
  - `Shift + Arrows` (`ShiftUp`, `ShiftDown`, `ShiftLeft`, `ShiftRight` and raw terminal escape sequences `\e[1;2A-D` / `\e[2A-D` / `\e[a-d`): Interactive text selection in all directions.
  - `Ctrl + Shift + Arrows` (`CtrlShiftLeft`, `CtrlShiftRight` and `\e[1;6C-D`): Word-by-word text selection.
  - `Shift + Home` / `Shift + End`: Select to beginning/end of line.
  - `Ctrl-b`: Toggles the file manager tree sidebar (`tree` command).
  - `Ctrl-p`: Triggers the `fzf` fuzzy file searcher for quick file opening.
  - `Alt-l`: Triggers the interactive code linter (`command:lint`) to check syntax/compilation errors.
  - `CtrlLeft` / `CtrlRight`, `Alt-Left` / `Alt-Right`: Word-by-word cursor navigation.
  - `Ctrl-Backspace`, `Alt-Backspace`, `Ctrl-w`, `Ctrl-h`: Deletes the previous word for rapid terminal text editing.

- **`settings.json`**:
  Optimized terminal editor settings:
  - `"clipboard": "external"`: Integrates with the system X11 clipboard via `xclip`, ensuring reliable `Ctrl-c` copy and `Ctrl-v` paste operations between Micro and external applications.
  - `"smartpaste": true`: Intelligently formats leading indentation when pasting multi-line text blocks.
  - `"autoindent": false`, `"keepautoindent": false`: Prevents compound indentation staircasing during external terminal/SSH pastes.
  - `"colorscheme": "monokai"`: High-contrast developer-friendly color theme.
  - `"cursorline": true`, `"ruler": true`, `"scrollbar": true`: Visual navigation cues and line numbering.
  - `"hlsearch": true`, `"incsearch": true`: Incremental and highlighted search matching.
  - `"rmtrailingws": true`: Automatically strips trailing whitespace on save.
  - `"saveundo": true`: Preserves undo history across editor sessions.
  - `"softwrap": true`, `"wordwrap": true`: Visual word-boundary line wrapping for long lines while preserving logical line structure and numbers without altering file content.
  - `"linter": true`: Enables real-time code and syntax verification for Python (`flake8`, `pyflakes`) and C (`gcc -fsyntax-only`), displaying error markers (`>>`) directly on the offending line before execution.
  - `"autocomplete_tooltip.EnableCursorUpDown": true`: Enables `Up` and `Down` arrow key cycling through completion candidates in the interactive autocomplete tooltip popup.
  - `"tabsize": 4`, `"tabstospaces": true`: 4-space indentation standard.
  - `"statusformatl"`: Informative status line displaying file name, modification status, cursor coordinates, filetype, and encoding.
  - `"autoclose": true`: Automatically closes braces and quotes.
  - `"filemanager-openonstart": false`: Keeps editor uncluttered on initial file open.
  - `"openbftype": "tab"`: Avoids multi-pane split views on file picks; opens files directly into active buffer (or new tab if buffer is populated).

- **`colorschemes/`**:
  Directory containing custom colorschemes (`monokai.micro`), providing dedicated styling for the autocomplete tooltip popup window and syntax/linter gutter highlights.

- **`plug/`**:
  Directory containing productivity plugins (`filemanager`, `editorconfig`, `fzf`, `bookmark`, `snippets`, `micro-autocomplete-tooltip`).

