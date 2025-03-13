# Ajoutez en fin de fichier avant le main()
def create_app():
    return Application.builder().token(TELEGRAM_TOKEN).build()

# Modifiez la fonction main()
def main():
    if not TELEGRAM_TOKEN or not HF_TOKEN:
        raise ValueError("Tokens manquants!")
    
    app = create_app()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Configuration webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=os.environ.get("WEBHOOK_URL", "https://isticharabot-koyeb.app/webhook"),
        max_connections=50
    )

if __name__ == "__main__":
    main()
