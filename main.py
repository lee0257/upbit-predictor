from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_telegram_message(message: str):
    print("[텔레그램] 전송 시도")
    if not TELEGRAM_TOKEN or not CHAT_IDS:
        print("[텔레그램 오류] 설정 누락")
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
    print("[슬랙] 전송 시도")
    if not SLACK_WEBHOOK_URL:
        print("[슬랙 오류] 설정 누락")
        return
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        print("슬랙 응답:", response.status_code, response.text)
    except Exception as e:
        print(f"[슬랙 오류] {e}")

@app.get("/")
def root():
    print("[/] 엔드포인트 호출됨")
    return {"status": "OK", "message": "서버 연결되었습니다 ✅"}

@app.post("/send-message")
async def send_message(request: Request):
    print("[/send-message] 호출됨")
    try:
        data = await request.json()
        message = data.get("message", "")
        print(f"수신 메시지: {message}")

        if not message:
            print("[오류] 메시지 비어 있음")
            return {"status": "fail", "message": "❌ 메시지가 비어 있습니다"}

        send_telegram_message(message)
        send_slack_message(message)

        return {"status": "success", "message": "✅ 메시지 전송 완료"}
    except Exception as e:
        print(f"[서버 오류] {e}")
        return {"status": "fail", "message": f"❌ 서버 오류: {e}"}
