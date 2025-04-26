import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Comando /start: quando o usuário envia o comando "/start"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Envia uma mensagem de boas-vindas ao usuário
    await update.message.reply_text("Salve! Eu sou o Chatbot da FURIA! 🦁 Manda uma mensagem aí!")

# Quando o usuário manda uma mensagem de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtém a mensagem do usuário e converte para minúsculas para facilitar a comparação
    user_message = update.message.text.lower()

    # Condições para diferentes respostas dependendo do conteúdo da mensagem
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
        # Caso a mensagem não tenha sido reconhecida, o bot responde genericamente
        reply = "Não entendi muito bem, mas tamo junto, FURIA sempre! 🔥"

    # Responde ao usuário com a mensagem escolhida
    await update.message.reply_text(reply)

# Função principal que configura e inicia o bot
async def main():
    TOKEN = "7679241514:AAEcLXmiBoLNqriflJ9BCnWc3OOCFDane_w"  # Troque pelo seu token real!

    # Criação da aplicação do bot usando o token
    app = ApplicationBuilder().token(TOKEN).build()

    # Adiciona o handler para o comando /start
    app.add_handler(CommandHandler("start", start))

    # Adiciona o handler para mensagens de texto (exceto comandos)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Exibe uma mensagem no terminal para indicar que o bot está rodando
    print("Bot está rodando... 🐱‍👤")

    # Inicia o bot e aguarda mensagens
    await app.run_polling()

# Executa o bot com nest_asyncio aplicado para garantir compatibilidade com asyncio no ambiente
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
