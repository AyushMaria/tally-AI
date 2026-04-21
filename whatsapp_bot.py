import os
import threading
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from agent import run_agent
import requests

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # e.g. whatsapp:+14155238886
AUTHORIZED_NUMBERS = os.getenv("WHATSAPP_AUTHORIZED_NUMBERS", "").split(",")

app = Flask(__name__)

def send_whatsapp_message(to: str, text: str):
    from twilio.rest import Client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # Split if over 1600 chars (Twilio WhatsApp limit)
    for i in range(0, len(text), 1600):
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=to,
            body=text[i:i+1600]
        )

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    sender = request.form.get("From")   # e.g. "whatsapp:+919876543210"
    text = request.form.get("Body", "").strip()
    sender_number = sender.replace("whatsapp:", "")  # strip prefix for auth check

    print(f"📩 WhatsApp from {sender}: {text}")

    # Send immediate acknowledgment
    resp = MessagingResponse()
    resp.message("🔍 Fetching data, please wait...")

    if sender_number not in AUTHORIZED_NUMBERS:
        resp = MessagingResponse()
        resp.message("❌ Unauthorized.")
        return str(resp), 200

    # Process agent in background, send result separately
    def process():
        response = run_agent(text)
        send_whatsapp_message(sender, response)

    threading.Thread(target=process).start()

    return str(resp), 200

def run_whatsapp():
    app.run(port=5000, use_reloader=False)