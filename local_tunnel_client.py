import websocket
import requests
import urllib3
import json

# Disable warnings for self-signed certificates (if using HTTPS locally)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def on_message(ws, message):
    print("📩 Webhook payload received. Forwarding to .NET API...")

    # Validate JSON
    try:
        payload = json.loads(message)
    except json.JSONDecodeError:
        print("❌ Invalid JSON received")
        ws.send(json.dumps({"error": "Invalid JSON received"}))
        return

    # Call local .NET API
    try:
        response = requests.post(
            url="http://localhost:5000/api/webhook",
            json=payload,
            verify=False  # Allow self-signed certs for local development
        )
        print(f"✅ Response from .NET API: {response.text}")
        ws.send(response.text)
    except Exception as e:
        error_msg = f"❌ Failed to call local .NET API: {e}"
        print(error_msg)
        ws.send(json.dumps({"error": str(e)}))

def on_open(ws):
    print("🔌 Connected to Railway WebSocket tunnel")

def on_error(ws, error):
    print(f"❌ WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"🔌 WebSocket Closed: {close_status_code}, {close_msg}")

def run_ws():
    ws = websocket.WebSocketApp(
        url="wss://customtunnel-production.up.railway.app/ws/swapnil",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    run_ws()
