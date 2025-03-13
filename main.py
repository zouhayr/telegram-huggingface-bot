import os
import requests
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Charger les tokens AU NIVEAU GLOBAL
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-multilingual-cased"

def query_huggingface(text):
    # ... (garder le reste de la fonction inchangé)

def main():
    # Vérification DES VARIABLES GLOBALES
    if not TELEGRAM_TOKEN or not HF_TOKEN:
        print("Erreur : Tokens non configurés!")
        return
    
    # ... (reste du code main() inchangé)

if __name__ == "__main__":
    main()
