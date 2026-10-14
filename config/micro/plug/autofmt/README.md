# Auto Format & Code Positioning Plugin (`config/micro/plug/autofmt/`)

This directory contains the `autofmt` plugin for the Micro terminal text editor. It provides automated code positioning, indentation, and formatting for Python, C/C++, Rust, and other languages.

## Files & Purposes

- **`autofmt.lua`**:
  The core plugin implementation. Automatically resolves formatting tools (`clang-format`, `ruff`, `autopep8`, `black`, `rustfmt`) and provides:
  - **Smart Syntax Auto-Indentation**: Automatically indents new lines (+4 spaces / 1 tab) upon pressing `Enter` after block statements (`if`, `elif`, `else:`, `for`, `while`, `def`, `class`, `with`, `try:`, `except`, `finally:`, `match`, `case`) in Python, and after opening braces (`{`, `(`, `[`) in C, C++, Rust, and other languages.
  - **Part-of-code formatting**: When a code block is selected, formats only the selected lines using range formatters (`clang-format --lines=X:Y` for C/C++, `autopep8 --line-range X Y` for Python).
  - **Whole-file formatting**: When no text is selected, formats the entire file.
  - **Format on save**: Automatically formats files on save when `"autofmt.onsave": true`.
  - **Cursor restoration**: Remembers and restores exact cursor position after re-opening the formatted buffer.
  - **Commands**: Registers `format`, `fmt`, and `fmtfile`.

- **`repo.json`**:
  Plugin metadata and version manifest recognized by Micro's plugin loader.
