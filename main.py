import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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
def start(update, context):
    update.message.reply_text("Bienvenue! Envoie-moi un message.")

# Réponse aux messages avec Hugging Face
def echo(update, context):
    user_message = update.message.text
    hf_response = query_huggingface(user_message)
    update.message.reply_text(f"Réponse de Hugging Face : {hf_response}")

def main():
    # Initialiser le bot
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Ajouter les handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Démarrer le bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


