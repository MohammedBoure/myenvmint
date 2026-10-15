# XFCE4 Configuration (`config/xfce4/`)

This directory houses the exported XFCE desktop environment and terminal configuration channels.

## Structure & Purposes

- **`xfconf/xfce-perchannel-xml/`**:
  Stores all Xfconf XML channels including:
  - `xfce4-terminal.xml`: Terminal styling, font size, transparent background (`#2e2e2e2e3333`), and ibeam cursor.
  - `displays.xml`: Dual-monitor configuration profiles (`LVDS-1` primary at 1920x1080, `VGA-1-1` secondary at 1024x768).
  - `xsettings.xml`: GTK themes (`Mint-L-Dark-Aqua`) and icon sets (`ePapirus`).
  - `keyboard-layout.xml` & `xfce4-keyboard-shortcuts.xml`: Layout toggle options, Super key Whisker Menu integration, and suppression of conflicting xfwm4 keypad workspace grabs to allow sxhkd unified window management.
  - `xfwm4.xml`: Window manager settings, configuring 10 workspaces and the `MyEnvMint-Dark` theme with visible window borders.
  - `xfce4-panel.xml`: Single bottom panel configuration with intelligent hover autohide (`autohide-behavior` 2, position `p=10`), Whisker Menu (`whiskermenu`), tasklist, pager, system tray, and status plugins.
- **`panel/`**:
  Contains XFCE panel launcher configurations and desktop shortcuts.
