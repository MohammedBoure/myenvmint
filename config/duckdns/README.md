# DuckDNS Configuration (`config/duckdns/`)

This directory contains configuration templates for the DuckDNS Dynamic DNS automatic IP update service.

## Files & Purposes

- **`duckdns.env.example`**:
  Template environment file defining `DUCKDNS_DOMAIN` and `DUCKDNS_TOKEN`. It guides users on configuring their secret credentials in `~/.config/duckdns/duckdns.env` (with restricted permissions `600`) without exposing tokens to version control.
