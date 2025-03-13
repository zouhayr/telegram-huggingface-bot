import os
import requests
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration globale
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert/distilbert-base-multilingual-cased"

# Fonction pour interroger Hugging Face
def query_huggingface(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"Erreur API : {e}, Statut : {response.status_code if 'response' in locals() else 'inconnu'}, Réponse : {response.text if 'response' in locals() else 'inconnue'}"
        print(error_msg)
        return {"error": "Désolé, l'API Hugging Face est temporairement indisponible. Réessayez plus tard."}
    except ValueError:
        error_msg = f"Réponse JSON invalide : {response.text if 'response' in locals() else 'inconnue'}"
        print(error_msg)
        return {"error": "Erreur interne de l'API. Réessayez plus tard."}

# Commande /start
async def start(update, context):
    await update.message.reply_text("Bienvenue ! Envoyez-moi un message en arabe, darija ou français.")

# Réponse aux messages avec Hugging Face
async def echo(update, context):
    user_message = update.message.text
    print(f"Message reçu : {user_message}")
    response = query_huggingface(user_message)
    await update.message.reply_text(str(response)[:4000])

# Gestion des erreurs
async def error_handler(update, context):
    print(f"Une erreur est survenue : {context.error}")
    if update and update.message:
        await update.message.reply_text("Désolé, une erreur est survenue. Veuillez réessayer plus tard.")

# Fonction pour lancer le bot Telegram
async def run_bot():
    if not TELEGRAM_TOKEN or not HF_TOKEN:
        print("Configuration manquante !")
        return
    print(f"TELEGRAM_TOKEN utilisé : {TELEGRAM_TOKEN}")
    try:
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        application.add_error_handler(error_handler)
        print("Démarrage du bot...")
        await application.run_polling(timeout=20)
    except Exception as e:
        print(f"Erreur lors du démarrage : {e}")

# Endpoint Flask pour health check
@app.route('/health')
def health_check():
    return "OK", 200

# Lancer le bot dans le thread principal
if __name__ == "__main__":
    # Créer une boucle d'événements pour le thread principal
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
