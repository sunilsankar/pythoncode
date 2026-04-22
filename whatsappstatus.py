#!/usr/bin/env python3
#date 20-April-2026
#https://github.com/avoylenko/wwebjs-api
import requests
import json

STATUS_URL = "http://192.168.1.12:5000/session/status/sunil"
ALERT_URL = "https://xxxx.xx.xxx:8443/check-whatsapp"
EXPECTED_RESPONSE = {
    "success": True,
    "state": "CONNECTED",
    "message": "session_connected"
}

headers = {
    "accept": "application/json",
}
def check_whatsapp_status():
    try:
        response = requests.get(STATUS_URL, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        # strict validation
        if data == EXPECTED_RESPONSE:
            return True, data

        return False, data

    except (requests.RequestException, ValueError) as e:
        return False, str(e)
def send_alert(status_data):
    try:
        payload = f"WhatsApp is down\nResponse:\n{json.dumps(status_data, indent=2)}"

        requests.post(
            ALERT_URL,
            data=payload,
            timeout=10
        )

    except requests.RequestException:
        pass
if __name__ == "__main__":
    ok, result = check_whatsapp_status()

    if not ok:
        send_alert(result)
