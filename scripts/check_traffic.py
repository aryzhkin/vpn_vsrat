#!/usr/bin/env python3
"""
Daily bandwidth monitor for vsrat-vpn droplet.
Sends email alerts at 50%, 85%, and 100% of monthly traffic limit.
Each alert is sent only once per month (state tracked in /root/.traffic_alerts_state).

Cron setup on the droplet:
  0 9 * * * set -a && source /root/.env_traffic && set +a && python3 /root/check_traffic.py >> /var/log/traffic_check.log 2>&1
"""

import os
import json
import urllib.request
import smtplib
import calendar
from datetime import datetime, timezone
from email.mime.text import MIMEText

# --- Config ---
DO_TOKEN        = os.getenv("DO_TOKEN", "")
DROPLET_ID      = "557042178"
LIMIT_GB        = 1000
EMAIL_TO        = os.getenv("EMAIL_TO", "")
EMAIL_FROM      = os.getenv("EMAIL_FROM", "")
EMAIL_PASSWORD  = os.getenv("EMAIL_PASSWORD", "")
STATE_FILE      = "/root/.traffic_alerts_state"

THRESHOLDS = [
    (50,  "⚠️ Половина трафика израсходована"),
    (85,  "🔶 Осталось мало трафика"),
    (100, "🔴 Трафик исчерпан"),
]
# --------------

def do_api(path):
    req = urllib.request.Request(
        f"https://api.digitalocean.com/v2{path}",
        headers={"Authorization": f"Bearer {DO_TOKEN}"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def get_monthly_bandwidth_gb():
    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    path = (
        f"/monitoring/metrics/droplet/bandwidth"
        f"?host_id={DROPLET_ID}&interface=public&direction=outbound"
        f"&start={int(start.timestamp())}&end={int(now.timestamp())}"
    )
    data = do_api(path)
    values = data["data"]["result"][0]["values"]
    total_bytes = sum(float(v[1]) * 300 for v in values)
    return total_bytes / (1024 ** 3)

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def send_alert(pct, title, used_gb):
    remaining = max(0, LIMIT_GB - used_gb)
    subject = f"[vsrat-vpn] {title} ({pct}% / {used_gb:.0f} GB)"
    body = (
        f"{title}\n\n"
        f"Использовано:  {used_gb:.1f} GB  ({pct:.0f}%)\n"
        f"Осталось:      {remaining:.1f} GB\n"
        f"Лимит:         {LIMIT_GB} GB / месяц\n\n"
        f"Дроплет: vsrat-vpn (209.38.42.79)\n\n"
        f"При превышении лимита DO не отключает сервер, "
        f"но тарифицирует $0.01/GB сверху.\n"
        f"Проверить: https://cloud.digitalocean.com"
    )
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_FROM
    msg["To"]      = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print(f"  → Alert sent: {subject}")

def main():
    used_gb = get_monthly_bandwidth_gb()
    used_pct = (used_gb / LIMIT_GB) * 100
    now = datetime.now(timezone.utc)
    month_key = f"{now.year}-{now.month:02d}"

    now_str = now.strftime("%Y-%m-%d %H:%M")
    print(f"[{now_str}] Monthly outbound: {used_gb:.2f} GB ({used_pct:.1f}%) / {LIMIT_GB} GB")

    state = load_state()
    sent_this_month = state.get(month_key, [])

    for threshold_pct, title in THRESHOLDS:
        if used_pct >= threshold_pct and threshold_pct not in sent_this_month:
            if EMAIL_TO and EMAIL_FROM and EMAIL_PASSWORD:
                send_alert(threshold_pct, title, used_gb)
                sent_this_month.append(threshold_pct)
            else:
                print(f"  ! Threshold {threshold_pct}% reached but email not configured")

    state[month_key] = sent_this_month
    # Keep only current and previous month in state
    if now.month == 1:
        prev_month_key = f"{now.year - 1}-12"
    else:
        prev_month_key = f"{now.year}-{now.month - 1:02d}"
    state = {k: v for k, v in state.items() if k >= prev_month_key}
    save_state(state)

    remaining = max(0, LIMIT_GB - used_gb)
    print(f"  Remaining: {remaining:.1f} GB | Alerts sent this month: {sent_this_month}")

if __name__ == "__main__":
    main()
