from flask import Flask
import os
import requests

app = Flask(__name__)

# Fetching the Telegram tokens securely from Render environment variables
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API_ID = os.environ.get("TELEGRAM_API_ID")
API_HASH = os.environ.get("TELEGRAM_API_HASH")

@app.route('/')
def home():
    # Simple check to verify Render sees your token
    if BOT_TOKEN:
        return "Scene Movie HD Service is running! Telegram Token is configured securely."
    else:
        return "Scene Movie HD Service is running, but TELEGRAM_BOT_TOKEN is missing in Render settings."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
