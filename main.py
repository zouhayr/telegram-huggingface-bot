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
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"Erreur API : {e}, Statut : {response.status_code}, Réponse : {response.text}"
        print(error_msg)
        return {"error": error_msg}
    except ValueError:
        error_msg = f"Réponse JSON invalide : {response.text}"
        print(error_msg)
        return {"error": error_msg}

# Commande /start
def start(update, context):
    update.message.reply_text("Bienvenue! Envoie-moi un message.")

# Réponse aux messages avec Hugging Face
def echo(update, context):
    user_message = update.message.text
    hf_response = query_huggingface(user_message)
    update.message.reply_text(f"Réponse de Hugging Face : {hf_response}")

# Gestion des erreurs
def error_handler(update, context):
    print(f"Une erreur est survenue : {context.error}")
    if update:
        update.message.reply_text("Désolé, une erreur est survenue. Veuillez réessayer plus tard.")

def main():
    if not TELEGRAM_TOKEN:
        print("Erreur : TELEGRAM_TOKEN n'est pas défini.")
        return
    try:
        updater = Updater(TELEGRAM_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        dp.add_error_handler(error_handler)
        print("Démarrage du bot...")
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(f"Erreur lors du démarrage : {e}")

if __name__ == "__main__":
    main()
