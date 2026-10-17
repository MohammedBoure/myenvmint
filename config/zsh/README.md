# Zsh Configuration (`config/zsh/`)

This directory houses the user shell configuration for Zsh.

## Files & Purposes

- **`zshrc`**:
  The master `~/.zshrc` configuration file. Features:
  - UTF-8 locale and environment exports (`PATH` including `~/.local/bin`, default editor).
  - Robust history management (10,000 entries, duplicate filtering, shared history across open terminals).
  - History-First Interactive Menu matching PowerShell ListView UX: when typing a command prefix (e.g. `ls`, `git`), displays matching historical lines directly in a vertical dropdown list tagged with yellow `[History]`.
  - Driven by `zmodload zsh/complist` with `_history_lines_first` at the head of the completer chain, evaluating history before filenames and system commands.
  - Interactive navigation through past commands via Arrow keys (`Up` / `Down`) or `<Tab>` / `<Shift-Tab>`, and instant execution via `<Enter>`.
  - Arrow keys (`Up` / `Down`) prefix substring history search (`up-line-or-beginning-search`).
  - Integration with `zsh-autosuggestions` and `zsh-syntax-highlighting`.
  - Integration with `fzf` for fuzzy popup command history (`Ctrl+R`) and directory navigation (`Alt+C`).
  - Desktop opener aliases: `start`, `open`, and `explorer` to instantly open the current terminal path in the GUI file manager (Nemo/Thunar).
  - Starship prompt initialization hook (`eval "$(starship init zsh)"`).
  - Zellij intelligent session workflow: Smart `zellij` wrapper preventing accidental/unwanted session generation (attaches to the sole active session if 1 exists, opens SessionX picker if multiple exist, or prompts before creation if 0 exist). Provides explicit session creators `zn [name]` / `zc [name]` / `zellij new [name]`, smart attach `zj` and `za [session]`, `zls` (list sessions), `zk <session>` (kill session), `zka` (kill all), and SSH auto-attach (`ZELLIJ_AUTO_ATTACH=1`).
- **`zshenv`**:


  Pre-initialization environment setting `skip_global_compinit=1` to prevent Ubuntu global shell profiles from conflicting with modern completion frameworks.
