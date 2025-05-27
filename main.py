from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_telegram(message):
    print("[텔레그램] 전송 시작")
    try:
        for chat_id in CHAT_IDS:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            res = requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=5)
            print("텔레그램 응답:", res.status_code, res.text)
    except Exception as e:
        print("[텔레그램 오류]", e)

def send_slack(message):
    print("[슬랙] 전송 시작")
    try:
        res = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=5)
        print("슬랙 응답:", res.status_code, res.text)
    except Exception as e:
        print("[슬랙 오류]", e)

@app.post("/send-message")
async def send_message(request: Request):
    print("[/send-message] 호출됨")
    try:
        data = await request.json()
        msg = data.get("message", "")
        print("전송 메시지:", msg)
        send_telegram(msg)
        send_slack(msg)
        return {"status": "ok"}
    except Exception as e:
        print("[전체 실패]", e)
        return {"status": "fail", "error": str(e)}
