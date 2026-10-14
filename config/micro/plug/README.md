# Micro Plugins Directory (`config/micro/plug/`)

This directory contains installed productivity plugins for the Micro text editor.

## Plugins & Purposes

- **`filemanager/`**:
  A file manager tree explorer plugin for Micro allowing sidebar navigation (`Ctrl-b`). Configured to automatically close the sidebar and open the chosen file directly on the active buffer without creating vertical/horizontal split panes.

- **`fzf/`**:
  Fuzzy file finder integration using `fzf` to quickly search and open files via `Ctrl-p` or the `fzf` command. Configured to run interactively and open selections directly via standard `open`/`tab` commands without spawning split terminal panes.

- **`editorconfig/`**:
  EditorConfig integration automatically setting indent styles, tab sizes, and trimming trailing whitespace based on `.editorconfig`.

- **`bookmark/`**:
  Line bookmarking plugin allowing users to bookmark lines (`toggleBookmark` / `Ctrl-F2`) and jump between saved positions (`nextBookmark` / `F2`).

- **`snippets/`**:
  Code snippets manager providing tab-triggered snippet expansion across dozens of programming languages.

- **`micro-autocomplete-tooltip/`**:
  Interactive dropdown/tooltip completion plugin for Micro. When pressing `Tab` in the buffer or command prompt (`Ctrl-e`), renders an inline tooltip menu displaying candidate matches, navigable with `Up` and `Down` arrow keys.

- **`autofmt/`**:
  Automated code positioning and formatting plugin for Micro supporting Python, C/C++, Rust, and other languages. Supports partial-selection formatting, whole-file formatting, and automatic formatting on save.

- **`lsp/`**:
  Language Server Protocol (LSP) client for Micro. Integrates with industry-standard language servers (`pylsp` / `pyright` for Python, `clangd` for C/C++, `rust-analyzer` for Rust) to deliver professional code completion (`Ctrl-Space`, `Tab`), definition navigation (`Alt-d`), type hover documentation (`Alt-k`), and references lookup (`Alt-r`).



