# Starship Configuration (`config/starship/`)

This directory houses the Starship cross-shell prompt configuration.

## Files & Purposes

- **`starship.toml`**:
  The Starship prompt theme configuration. Provides a clean, modern, and high-performance prompt displaying:
  - Current directory path with directory truncation and read-only indicators.
  - Git branch and repository status (staged, modified, untracked).
  - Command duration timer for long-running processes.
  - Distinct colored prompt character symbols (`$` or `➜`) reflecting success or error exit codes.
