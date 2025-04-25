import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salve! Eu sou o Chatbot da FURIA! 🦁 Manda uma mensagem aí!")

# Quando o usuário manda uma mensagem de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    if "oi" in user_message:
        reply = "Fala, torcedor da FURIA! 💥"
    elif "seu time favorito" in user_message:
        reply = "É claro que é a FURIA, né! 🦁"
    elif "quando é o próximo jogo" in user_message:
        reply = "Fique ligado nas redes da FURIA, tem jogo em breve! 🎮"
    elif "qual seu nome" in user_message:
        reply = f"Meu nome é Chatbot FURIA! 😎"
    elif "como você está?" in user_message:
        reply = "Estou bem, obrigado! E você? 😁"
    else:
        reply = "Não entendi muito bem, mas tamo junto, FURIA sempre! 🔥"

    await update.message.reply_text(reply)

# Função principal que configura o bot
async def main():
    TOKEN = "7679241514:AAEcLXmiBoLNqriflJ9BCnWc3OOCFDane_w"  # Troque pelo seu token real!

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot está rodando... 🐱‍👤")
    await app.run_polling()

# Executa o bot com nest_asyncio aplicado
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
