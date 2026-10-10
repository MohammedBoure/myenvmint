#!/usr/bin/env python3
import os
import json
import datetime
import subprocess

CACHE_FILE = os.path.expanduser('~/.cache/traffic_today.json')

def get_boot_date():
    try:
        out = subprocess.check_output(['uptime', '-s'], stderr=subprocess.DEVNULL).decode().strip()
        return out.split()[0]
    except Exception:
        return ''

def get_current_bytes():
    rx_total = 0
    tx_total = 0
    try:
        with open('/proc/net/dev', 'r') as f:
            for line in f:
                if ':' in line:
                    parts = line.split(':')
                    iface = parts[0].strip()
                    if iface == 'lo':
                        continue
                    vals = parts[1].split()
                    if len(vals) >= 9:
                        rx = int(vals[0])
                        tx = int(vals[8])
                        rx_total += rx
                        tx_total += tx
    except Exception:
        pass
    return rx_total, tx_total

def get_vnstat_today():
    try:
        out = subprocess.check_output(['vnstat', '--json', 'd', '1'], stderr=subprocess.DEVNULL).decode()
        data = json.loads(out)
        total_b = 0
        for iface in data.get('interfaces', []):
            days = iface.get('traffic', {}).get('day', [])
            if days:
                today_entry = days[-1]
                total_b += today_entry.get('rx', 0) + today_entry.get('tx', 0)
        return total_b
    except Exception:
        return 0

def format_bytes(b):
    if b < 1024:
        return f'{b} B'
    elif b < 1024 * 1024:
        return f'{b / 1024:.1f} KB'
    elif b < 1024 * 1024 * 1024:
        return f'{b / (1024 * 1024):.1f} MB'
    else:
        return f'{b / (1024 * 1024 * 1024):.2f} GB'

def main():
    today_str = datetime.date.today().isoformat()
    boot_date = get_boot_date()
    rx, tx = get_current_bytes()
    curr_total = rx + tx

    data = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
        except Exception:
            pass

    if data.get('date') != today_str:
        accumulated = 0
        base_total = 0 if boot_date == today_str else curr_total
        data = {
            'date': today_str,
            'base_total': base_total,
            'accumulated': accumulated,
            'last_total': curr_total
        }
    else:
        last = data.get('last_total', curr_total)
        if curr_total < last:
            # Reboot occurred
            data['accumulated'] += max(0, last - data.get('base_total', 0))
            data['base_total'] = 0
        data['last_total'] = curr_total

    today_proc = data['accumulated'] + (curr_total - data['base_total'])
    vnstat_b = get_vnstat_today()
    final_today = max(today_proc, vnstat_b)

    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass

    print(f"{format_bytes(final_today)}")

if __name__ == '__main__':
    main()
