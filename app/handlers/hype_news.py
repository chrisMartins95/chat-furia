# Importação das bibliotecas necessárias
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.hype_news_service import buscar_hype_news  # Importa função para buscar notícias

# Função principal para enviar as notícias
async def enviar_hype_news(bot: Bot, chat_id: int):
    # Busca as últimas notícias sobre a FURIA
    noticias = buscar_hype_news()

    # Caso não haja notícias, envia uma mensagem padrão
    if not noticias:
        await bot.send_message(chat_id, "Ainda não temos novidades fresquinhas da FURIA. Fica de olho que vem coisa boa por aí!")
        return

    # Envia cada notícia encontrada
    for noticia in noticias:
        mensagem = f"🔥 {noticia['titulo']}\n\n{noticia['resumo']}\n\nLeia mais: {noticia['url']}"
        await bot.send_message(chat_id, mensagem)
    
    # Cria o botão "Voltar ao menu principal"
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envia a mensagem perguntando se o usuário deseja voltar ao menu
    await bot.send_message(
        chat_id,
        "🔙 Quer voltar pro menu principal, tropa?",
        reply_markup=reply_markup
    )
