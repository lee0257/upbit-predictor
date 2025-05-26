from fastapi import FastAPI
import asyncio
import json
import websockets
import requests
import time
from datetime import datetime, timedelta
import os
import threading

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

print("🚀 슬랙 실전 급등 포착 시스템 시작")
print("✅ 환경변수 SLACK_WEBHOOK_URL =", SLACK_WEBHOOK_URL)  # 여기에 찍힌다

coin_meta = {}
base_prices = {}
volume_window = {}
strength_window = {}
last_sent = {}

EXCLUDED_COINS = {"KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE"}

def send_slack_message(msg):
    payload = {"text": msg}
    try:
        res = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        print(f"📤 슬랙 전송 응답: {res.status_code} - {res.text}")
    except Exception as e:
        print("❌ 슬랙 전송 실패:", e)

# 아래 코드 동일. 간결하게 생략 가능
# ...

app = FastAPI()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_background_task)
    thread.daemon = True
    thread.start()

@app.get("/")
def root():
    return {"status": "OK", "message": "슬랙 실전 전략 서버 작동 중 ✅"}

@app.get("/test")
def test():
    send_slack_message("✅ *슬랙 알림 테스트 메시지입니다.* 시스템 작동 확인용.")
    return {"status": "sent"}
