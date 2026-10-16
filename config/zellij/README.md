# Zellij Configuration (`config/zellij/`)

This directory houses the user configuration for the Zellij Terminal Multiplexer.

## Files & Purposes

- **`config.kdl`**:
  The primary configuration file for Zellij in KDL format:
  - **Micro Editor Compatibility**: Remaps the global Quit action from `Ctrl + q` to `Ctrl + Alt + q` (and `Ctrl + o` then `q` in session mode) so that `Ctrl + q` passes directly through to nested editors (such as Micro) without accidentally terminating the Zellij session.
  - **OSC 52 Clipboard & SIGINT Prevention**: Explicitly binds `Ctrl + Shift + c` and `Alt + c` to `Copy` across normal, scroll, and search modes, copying selections directly to the local system clipboard via OSC 52 without forwarding `\x03` (SIGINT) to running terminal processes. Enables `copy_on_select true` and `copy_clipboard "system"`.
  - **Rendering & Theme Legibility**: Sets `simplified_ui true` to replace missing powerline/nerd-font arrow glyphs with clean, universal Unicode/ASCII borders. Applies the balanced `catppuccin-mocha` dark theme for optimal readability over remote SSH sessions.
  - **Session Management & SessionX Integration**:
    - **SessionX Plugin**: Replaces the default session manager with the SessionX plugin (`sessionx location="zellij:session-manager"` configured for single-screen unified session view).
    - **Ergonomic Keybindings**: Binds `Ctrl + o` then `w` (in session mode) and provides a direct, ergonomic global shortcut `Alt + s` across all unlocked modes (`shared_except "locked"`) to instantly launch or focus the floating SessionX interface.
    - **Quick Actions**: Lists all sessions including the active/current session clearly (marked with current status and details) with quick actions:
      - Attach / Switch: Press `Enter` on the selected session.
      - Rename: Press `Ctrl + r` to rename on the fly.
      - Kill / Delete: Press `Delete` to delete/kill the selected session, or `Ctrl + d` to prompt for killing other sessions.
    - Preserves sessions on disconnect via `on_force_close "detach"`, and provides `Alt + d` (and `Ctrl + o` -> `d`) for instant background detaching.

