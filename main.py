import os
import requests
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Charger les tokens depuis les variables d'environnement
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-multilingual-cased"  # Correction de l'URL

# Fonction pour interroger Hugging Face
def query_huggingface(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Lève une exception pour les codes 4xx/5xx
        
        # Traitement de la réponse
        if isinstance(response.json(), list) and len(response.json()) > 0:
            return response.json()[0].get('generated_text', 'Réponse non reconnue')
        return response.json()
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Erreur API : {e}"
        if hasattr(e, 'response') and e.response:
            error_msg += f", Statut : {e.response.status_code}, Réponse : {e.response.text[:200]}"
        print(error_msg)
        return f"Erreur de traitement : {error_msg}"
    
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return "Erreur de traitement"

# Commande /start
async def start(update, context):
    await update.message.reply_text("Bienvenue! Envoie-moi un message.")

# Réponse aux messages avec Hugging Face
async def echo(update, context):
    user_message = update.message.text
    hf_response = query_huggingface(user_message)
    await update.message.reply_text(f"Réponse : {hf_response}")  # Formatage simplifié

# Gestion des erreurs
async def error_handler(update, context):
    print(f"Erreur : {context.error}")
    if update:
        await update.message.reply_text("Désolé, problème technique. Réessayez plus tard.")

def main():
    if not TELEGRAM_TOKEN or not HF_TOKEN:
        print("Erreur : Tokens non définis!")
        return
    
    try:
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        application.add_error_handler(error_handler)
        
        print("Démarrage du bot...")
        application.run_polling()
        
    except Exception as e:
        print(f"Erreur critique : {e}")

if __name__ == "__main__":  # Correction de l'espace superflu
    main()
