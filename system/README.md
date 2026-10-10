# System Configurations (`system/`)

This directory contains system-level configuration backups and templates applied to the host operating system.

## Files & Purposes

- **`keyboard.conf`**:
  Template for `/etc/default/keyboard`. Configures native French (AZERTY) and Arabic keyboard models, layout switching with `grp:win_space_toggle`, and console key mappings.

- **`dconf_cinnamon.ini`**:
  An exported dump of Cinnamon desktop keybindings and dconf keys ensuring that modifier keys and panel shortcuts do not conflict with the window manager or layout switchers.

- **`xfconf_keyboard.txt`**:
  Text export of the XFCE keyboard configuration channel properties.

- **`xfconf_shortcuts.txt`**:
  Text backup of active XFCE keyboard shortcuts.
