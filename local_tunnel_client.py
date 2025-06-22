import websocket
import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def on_message(ws, message):
    print("📩 Webhook payload received. Forwarding to .NET API...")
    try:
        r = requests.post(
            "http://localhost:5000/api/webhook",
            json=json.loads(message),
            verify=False
        )
        print(f"✅ Response from .NET API: {r.text}")
    except Exception as e:
        print(f"❌ Failed to call local .NET API: {e}")

def on_open(ws):
    print("🔌 Connected to Railway WebSocket tunnel")

def on_error(ws, error):
    print(f"❌ WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"🔌 WebSocket Closed: {close_status_code}, {close_msg}")

def run_ws():
    ws = websocket.WebSocketApp(
        "wss://customtunnel-production.up.railway.app/ws/swapnil",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    run_ws()
