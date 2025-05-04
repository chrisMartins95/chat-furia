# app/handlers/hype_news.py

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.hype_news_service import buscar_hype_news

async def enviar_hype_news(bot: Bot, chat_id: int):
    noticias = buscar_hype_news()

    if not noticias:
        await bot.send_message(chat_id, "Ainda não temos novidades fresquinhas da FURIA. Fica de olho que vem coisa boa por aí!")
        return

    for noticia in noticias:
        mensagem = f"🔥 {noticia['titulo']}\n\n{noticia['resumo']}\n\nLeia mais: {noticia['url']}"
        await bot.send_message(chat_id, mensagem)
        
    
     # Cria botão "Voltar ao menu principal"
    keyboard = [[InlineKeyboardButton("🔙 Voltar ao menu principal", callback_data="voltar_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(
        chat_id,
        "🔙 Quer voltar pro menu principal, tropa?",
        reply_markup=reply_markup
    )