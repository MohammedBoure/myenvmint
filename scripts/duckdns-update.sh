#!/usr/bin/env bash
# ==============================================================================
# DuckDNS Dynamic DNS IP Auto-Updater
# Fetches current public IP and updates the configured DuckDNS domain.
# ==============================================================================

set -e

# Load credentials from user config or local env file if not already set in environment
if [ -z "$DUCKDNS_DOMAIN" ] || [ -z "$DUCKDNS_TOKEN" ]; then
    if [ -f "$HOME/.config/duckdns/duckdns.env" ]; then
        # shellcheck disable=SC1090
        source "$HOME/.config/duckdns/duckdns.env"
    elif [ -f "$HOME/Desktop/myenvmint/.env" ]; then
        # shellcheck disable=SC1090
        source "$HOME/Desktop/myenvmint/.env"
    fi
fi

if [ -z "$DUCKDNS_DOMAIN" ] || [ -z "$DUCKDNS_TOKEN" ]; then
    echo "[DuckDNS Error] Missing DUCKDNS_DOMAIN or DUCKDNS_TOKEN environment variables." >&2
    exit 1
fi

LOG_DIR="$HOME/.local/state/duckdns"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/duckdns.log"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

# Perform update request to DuckDNS (omitting IP allows DuckDNS to auto-detect public IPv4)
RESPONSE=$(curl -fsS -m 30 "https://www.duckdns.org/update?domains=${DUCKDNS_DOMAIN}&token=${DUCKDNS_TOKEN}&ip=" 2>&1)

if [ "$RESPONSE" = "OK" ]; then
    MSG="[$TIMESTAMP] DuckDNS IP updated successfully for domain: ${DUCKDNS_DOMAIN}.duckdns.org (Response: OK)"
    echo "$MSG"
    echo "$MSG" >> "$LOG_FILE"
    exit 0
else
    MSG="[$TIMESTAMP] [DuckDNS Error] Update failed for domain: ${DUCKDNS_DOMAIN}.duckdns.org (Response: $RESPONSE)"
    echo "$MSG" >&2
    echo "$MSG" >> "$LOG_FILE"
    exit 1
fi
