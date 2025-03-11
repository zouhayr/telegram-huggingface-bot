import os
import requests
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Charger les tokens depuis les variables d'environnement
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"

# Fonction pour interroger Hugging Face
def query_huggingface(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

# Commande /start
async def start(update, context):
    await update.message.reply_text("Bienvenue! Envoie-moi un message.")

# Réponse aux messages avec Hugging Face
async def echo(update, context):
    user_message = update.message.text
    hf_response = query_huggingface(user_message)
    await update.message.reply_text(f"Réponse de Hugging Face : {hf_response}")

def main():
    # Initialiser le bot avec Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Ajouter les handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Démarrer le bot
    application.run_polling()

if __name__ == "__main__":
    main()

