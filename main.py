from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")  # 쉼표로 구분된 다중 ID
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not CHAT_IDS:
        print("[텔레그램] 설정 누락")
        return
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id.strip(),
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            print("텔레그램 응답:", response.status_code, response.text)
        except Exception as e:
            print(f"[텔레그램 오류] {e}")

def send_slack_message(message: str):
    if not SLACK_WEBHOOK_URL:
        print("[슬랙] 설정 누락")
        return
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        print("슬랙 응답:", response.status_code, response.text)
    except Exception as e:
        print(f"[슬랙 오류] {e}")

@app.get("/")
def root():
    return {"status": "OK", "message": "서버 연결되었습니다 ✅"}

@app.post("/send-message")
async def send_message(request: Request):
    data = await request.json()
    message = data.get("message", "")

    if not message:
        return {"status": "fail", "message": "❌ 메시지가 비어 있습니다"}

    send_telegram_message(message)
    send_slack_message(message)

    return {"status": "success", "message": "✅ 메시지 전송 완료"}
