# Systemd User Services (`config/systemd/user/`)

This directory houses systemd user units managed by `systemctl --user`.

## Files & Purposes

- **`barrier-client.service`**:
  Manages the Barrier KVM background client daemon (`barrierc`). Ensures the client starts automatically on session initialization and restarts gracefully upon network interruptions or keymap updates.
