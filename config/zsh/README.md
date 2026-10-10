# Zsh Configuration (`config/zsh/`)

This directory houses the user shell configuration for Zsh.

## Files & Purposes

- **`zshrc`**:
  The master `~/.zshrc` configuration file. Features:
  - UTF-8 locale and environment exports (`PATH` including `~/.local/bin`, default editor).
  - Robust history management (10,000 entries, duplicate filtering, shared history across open terminals).
  - Real-time predictive vertical completion menu via `zsh-autocomplete` with source/metadata tags (`[History]`, `[Command]`, `[Alias]`) and Tab/Arrow navigation.
  - Integration with `zsh-autosuggestions` and `zsh-syntax-highlighting`.
  - Integration with `fzf` for fuzzy popup command history (`Ctrl+R`) and directory navigation.
  - Starship prompt initialization hook (`eval "$(starship init zsh)"`).
- **`zshenv`**:
  Pre-initialization environment setting `skip_global_compinit=1` to prevent Ubuntu global shell profiles from conflicting with modern completion frameworks.
