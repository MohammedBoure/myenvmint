# Zsh Configuration (`config/zsh/`)

This directory houses the user shell configuration for Zsh.

## Files & Purposes

- **`zshrc`**:
  The master `~/.zshrc` configuration file. Features:
  - UTF-8 locale and environment exports (`PATH` including `~/.local/bin`, default editor).
  - Robust history management (10,000 entries, duplicate filtering, shared history across open terminals).
  - Interactive dropdown completion menu powered by `fzf-tab` with metadata/source groups (`[History]`, `[external command]`, `[alias]`, `[file]`) and directory preview (`ls -lah`).
  - Seamless navigation via `<Tab>` / `<Shift-Tab>` / Arrow keys, and instant `<Enter>` execution.
  - Battle-tested native Zsh completion fallback via `zmodload zsh/complist` with `menu select=1`.
  - Arrow keys (`Up` / `Down`) substring history search (`up-line-or-beginning-search`).
  - Integration with `zsh-autosuggestions` and `zsh-syntax-highlighting`.
  - Integration with `fzf` for fuzzy popup command history (`Ctrl+R`) and directory navigation (`Alt+C`).
  - Starship prompt initialization hook (`eval "$(starship init zsh)"`).
- **`zshenv`**:
  Pre-initialization environment setting `skip_global_compinit=1` to prevent Ubuntu global shell profiles from conflicting with modern completion frameworks.
