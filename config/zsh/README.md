# Zsh Configuration (`config/zsh/`)

This directory houses the user shell configuration for Zsh.

## Files & Purposes

- **`zshrc`**:
  The master `~/.zshrc` configuration file. Features:
  - UTF-8 locale and environment exports (`PATH` including `~/.local/bin`, default editor).
  - Robust history management (10,000 entries, duplicate filtering, shared history across open terminals).
  - Integration with `zsh-autosuggestions` for Fish-like asynchronous autocomplete.
  - Integration with `zsh-syntax-highlighting` for fast real-time command syntax coloring.
  - Integration with `fzf` for fuzzy command history and file navigation.
  - Starship prompt initialization hook (`eval "$(starship init zsh)"`).
