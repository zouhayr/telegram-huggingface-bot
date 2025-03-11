import os
import requests
import logging
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration des logs
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Récupération des tokens depuis les variables d'environnement
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"

# Vérifier si le token Telegram est défini
if not TELEGRAM_TOKEN:
    raise RuntimeError("Le token TELEGRAM_TOKEN est introuvable. Vérifiez votre configuration.")

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
    """Interroge l'API de Hugging Face et gère les erreurs."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and "error" in data:
            return "L'API Hugging Face a retourné une erreur."
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur de requête Hugging Face : {e}")
        return "Erreur de connexion à l'API Hugging Face."

async def check_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """S'assure que le bot ne répond que dans les messages privés."""
    if update.message.chat.type != "private":
        await update.message.reply_text("Je fonctionne uniquement en message privé.")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Répond au message /start uniquement en privé."""
    if await check_private_chat(update, context):
        await update.message.reply_text("Bienvenue! Envoie-moi un message.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Répète le message et envoie une réponse de Hugging Face."""
    if await check_private_chat(update, context):
        user_message = update.message.text
        hf_response = await query_huggingface(user_message)
        
        if isinstance(hf_response, list) and len(hf_response) > 0:
            reply_text = hf_response[0].get("generated_text", "Réponse non disponible.")
        else:
            reply_text = "Je n'ai pas pu comprendre la réponse de l'IA."
        
        await update.message.reply_text(f"Réponse de Hugging Face : {reply_text}")

async def main():
    """Démarre l'application Telegram en mode polling."""
    await clean_webhook()
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    logging.info("Démarrage du bot en mode polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


