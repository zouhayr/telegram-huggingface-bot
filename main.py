import os
import requests
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Configuration globale
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-multilingual-cased"

def query_huggingface(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Erreur : {str(e)}"

async def start(update, context):
    await update.message.reply_text("Bienvenue ! Envoyez-moi un message.")

async def echo(update, context):
    response = query_huggingface(update.message.text)
    await update.message.reply_text(str(response)[:4000])

def main():
    if not TELEGRAM_TOKEN or not HF_TOKEN:
        print("Configuration manquante !")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Démarrage...")
   app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=os.environ.get("WEBHOOK_URL"),
        max_connections=50
    )

if __name__ == "__main__":
    main()
