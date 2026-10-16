# Zellij Configuration (`config/zellij/`)

This directory houses the user configuration for the Zellij Terminal Multiplexer.

## Files & Purposes

- **`config.kdl`**:
  The primary configuration file for Zellij in KDL format:
  - **Micro Editor Compatibility**: Remaps the global Quit action from `Ctrl + q` to `Ctrl + Alt + q` (and `Ctrl + o` then `q` in session mode) so that `Ctrl + q` passes directly through to nested editors (such as Micro) without accidentally terminating the Zellij session.
  - **OSC 52 Clipboard & SIGINT Prevention**: Explicitly binds `Ctrl + Shift + c` and `Alt + c` to `Copy` across normal, scroll, and search modes, copying selections directly to the local system clipboard via OSC 52 without forwarding `\x03` (SIGINT) to running terminal processes. Enables `copy_on_select true` and `copy_clipboard "system"`.
  - **Rendering & Theme Legibility**: Sets `simplified_ui true` to replace missing powerline/nerd-font arrow glyphs with clean, universal Unicode/ASCII borders. Applies the balanced `catppuccin-mocha` dark theme for optimal readability over remote SSH sessions.
  - **Session Management**: Configures `on_force_close "detach"` to preserve sessions on disconnect, and binds `Alt + d` (as well as `Ctrl + o` -> `d`) for instant background detaching.

