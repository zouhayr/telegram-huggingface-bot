import os
import requests
import logging
import asyncio  # Ajout pour les fonctions async
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration des logs
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Récupération des tokens depuis les variables d'environnement
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"

# Vérifier si le token est bien défini
if not TELEGRAM_TOKEN:
    logging.error("Le token TELEGRAM_TOKEN est introuvable. Vérifiez votre configuration.")
    exit()

# Initialisation du bot Telegram
bot = Bot(TELEGRAM_TOKEN)

async def clean_webhook():
    """Supprime le webhook pour éviter les conflits avec le polling."""
    try:
        await bot.delete_webhook()
        logging.info("Webhook supprimé avec succès.")
    except Exception as e:
        logging.warning(f"Impossible de supprimer le webhook : {e}")

async def query_huggingface(text):
    """Interroge l'API de Hugging Face et retourne la réponse."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        logging.error(f"Erreur lors de la requête Hugging Face : {e}")
        return {"error": "Service indisponible"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Répond au message /start."""
    await update.message.reply_text("Bienvenue! Envoie-moi un message.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Répète le message et envoie une réponse de Hugging Face."""
    user_message = update.message.text
    hf_response = await query_huggingface(user_message)
    await update.message.reply_text(f"Réponse de Hugging Face : {hf_response}")

async def main():
    """Démarre l'application Telegram en mode polling."""
    await clean_webhook()  # Nettoyage du webhook avant de démarrer

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logging.info("Démarrage du bot en mode polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())  # Lancement correct de l'application


