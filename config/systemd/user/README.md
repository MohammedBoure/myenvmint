# Systemd User Services (`config/systemd/user/`)

This directory houses systemd user units managed by `systemctl --user`.

## Files & Purposes

- **`barrier-client.service`**:
  Manages the Barrier KVM background client daemon (`barrierc`). Ensures the client starts automatically on session initialization and restarts gracefully upon network interruptions or keymap updates.
- **`duckdns.service`**:
  One-shot service that executes `duckdns-update.sh` to update the public IP address for the configured DuckDNS domain using environment variables.
- **`duckdns.timer`**:
  Systemd calendar timer that triggers `duckdns.service` 1 minute after session startup and continuously every 5 minutes (`OnCalendar=*:0/5`) with persistent recovery across system suspensions and reboots.
- **`keepalive.service`**:
  Manages a persistent `systemd-inhibit` lock that blocks system idle, sleep, screensaver blanking, and automatic suspension, keeping the computer permanently active and awake.
