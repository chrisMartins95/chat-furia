from fastapi import FastAPI, Request
from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os

# Banco de dados
from app.database import create_db, save_message

# Modelos de dados
from app.models.fan_interaction import Fan, Interaction
from app.models.message import Message

# Handlers (funções para enviar menus e lidar com interações)
from app.handlers.telegram_menu import send_menu, handle_loja, handle_redes
from app.handlers.collect_user import start_collect_user_data, process_user_data, is_collecting

# Utilitários
from app.utils.validators import validate_age, validate_city
from app.utils.nlp_model import predict_intent

# Inicializações do ambiente
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Obtém o token do Telegram

# Inicializa o bot do Telegram com o token
bot = Bot(token=TELEGRAM_TOKEN)

# Inicia o FastAPI
app = FastAPI(
    title="Chatbot FURIA",  # Título da API
    description="Um chatbot para interagir com os torcedores da FURIA.",  # Descrição da API
    version="1.0.0"  # Versão da API
)

# Criação do banco de dados
create_db()

# Armazenamento temporário dos dados do usuário e controle de estados
user_data = {}  # Dicionário que armazena dados do usuário
user_state = {}  # Dicionário que armazena o estado atual de cada usuário

# Webhook do Telegram: endpoint que o Telegram chama quando há uma nova mensagem
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)  # Converte o JSON para um objeto Update do Telegram

    if update.message is None:
        return {"ok": True}
    
    message = update.message.text.strip()
    chat_id = update.message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = {}
        user_state[chat_id] = "ask_name"
        await bot.send_message(chat_id, "Fala torcedor da FURIA! 😎 Qual o seu nome?")
        return {"ok": True}
    
    state = user_state.get(chat_id)

    # Fluxo de coleta de dados
    if state == "ask_name":
        user_data[chat_id]["name"] = message
        user_state[chat_id] = "ask_age"
        await bot.send_message(chat_id, f"Boa, {message}! 🔥 Agora me diz: quantos anos você tem?")
    elif state == "ask_age":
        if not validate_age(message):
            await bot.send_message(chat_id, "Por favor, insira uma idade válida.")
        else:
            user_data[chat_id]["age"] = message
            user_state[chat_id] = "ask_city"
            await bot.send_message(chat_id, "Show! De qual cidade você fala?")
    elif state == "ask_city":
        if not validate_city(message):
            await bot.send_message(chat_id, "Por favor, insira uma cidade válida (apenas letras).")
        else:
            user_data[chat_id]["city"] = message
            user_state[chat_id] = "ask_nick"
            await bot.send_message(chat_id, "Legal! E qual o seu nick nos games?")
    elif state == "ask_nick":
        user_data[chat_id]["nickname"] = message
        user_state[chat_id] = "completed"
        await bot.send_message(chat_id, f"Fechou, {user_data[chat_id]['name']}! 🚀 Agora você é parte da nossa torcida! Vamos com tudo, FURIA!")
        await send_menu(bot, chat_id, welcome=False)
    elif message == "🛒 Loja da FURIA":
        await handle_loja(bot, chat_id)
        await send_menu(bot, chat_id, welcome=False)
    elif message == "🌐 Redes da tropa":
        await handle_redes(bot, chat_id)
        await send_menu(bot, chat_id, welcome=False)
    elif message == "🐱‍👤 Quem é a FURIA?":
        await handle_sobre_furia(bot, chat_id)
    elif message == "🐱‍👤 Falar sobre o time de CS":
        await handle_sobre_time_cs(bot, chat_id)
    elif message == "🎮 Falar sobre os jogadores":
        await handle_sobre_jogadores_cs(bot, chat_id)
    elif message in ["FalleN", "KSCERATO", "molodoy", "YEKINDAR", "yuurih", "Treinador-sidde","Treinador-Hepa"]:
        await handle_jogador_especifico(bot, chat_id, message)
    elif message == "🔙 Voltar ao menu principal":
        await send_menu(bot, chat_id, welcome=False)
    else:
        # Respostas baseadas em palavras-chave ou respostas simples
        if "loja" in message.lower():
            reply = "Acesse a Loja da FURIA aqui: [Link da loja]"
        elif "redes sociais" in message.lower():
            reply = "Você pode nos encontrar nas redes sociais: @furiaesports!"
        else:
            reply = "Desculpe, não entendi. Pode tentar de novo?"

        save_message(chat_id, message, reply)
        await bot.send_message(chat_id, reply)
        await send_menu(bot, chat_id, welcome=False)

    return {"ok": True}


async def handle_sobre_furia(bot: Bot, chat_id: int):
    """
    Envia informações sobre a FURIA quando o usuário escolhe a opção "Quem é a FURIA?".
    """
    info_furia = "Uma organização de esports que nasceu do desejo de representar o Brasil no CS 🇧🇷🎮 e conquistou muito mais que isso: expandimos nossas ligas 🌍, disputamos os principais títulos 🏆, adotamos novos objetivos 🎯 e ganhamos um propósito maior 💡. Somos muito mais que o sucesso competitivo. Somos um movimento sociocultural ✊🤝."
    await bot.send_message(chat_id=chat_id, text=info_furia)
    
    # Após mostrar a descrição, envia opções para o usuário
    menu_furia = ReplyKeyboardMarkup(
        [
            [KeyboardButton("🐱‍👤 Falar sobre o time de CS")],
            [KeyboardButton("🎮 Falar sobre os jogadores")],
            [KeyboardButton("🔙 Voltar ao menu principal")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    await bot.send_message(
        chat_id=chat_id,
        text="Agora que você conhece a FURIA, quer saber mais sobre o time ou os jogadores?",
        reply_markup=menu_furia
    )


async def handle_sobre_time_cs(bot: Bot, chat_id: int):
    """
    Envia informações sobre o time de CS quando o usuário escolhe a opção "Falar sobre o time de CS".
    """
    info_time = "O time de CS:GO da FURIA 🐯 é um dos mais temidos e respeitados no cenário mundial 🌍. Com um estilo de jogo agressivo e tático, a equipe conquistou diversos títulos internacionais 🏆 e se tornou uma das favoritas do público, representando o Brasil com muito orgulho 🇧🇷. Eles não apenas disputam grandes campeonatos, mas também deixam sua marca em cada evento com performances de tirar o fôlego 🔥. Com a liderança do experiente ART 🔫, a FURIA segue inovando e encantando fãs ao redor do mundo 💥!"
    await bot.send_message(chat_id=chat_id, text=info_time)
    
    # Após exibir as informações sobre o time de CS, envia novamente as opções
    menu_time_cs = ReplyKeyboardMarkup(
        [
            [KeyboardButton("🐱‍👤 Quem é a FURIA?")],
            [KeyboardButton("🎮 Falar sobre os jogadores")],
            [KeyboardButton("🔙 Voltar ao menu principal")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    await bot.send_message(
        chat_id=chat_id,
        text="Agora que você sabe sobre o time de CS, quer saber mais sobre os jogadores ou voltar?",
        reply_markup=menu_time_cs
    )

async def handle_sobre_jogadores_cs(bot: Bot, chat_id: int):
    """
    Envia informações sobre os jogadores do time de CS quando o usuário escolhe a opção "Falar sobre os jogadores".
    """
    # Informações básicas sobre os jogadores
    info_jogadores = "Aqui estão os jogadores da FURIA! Escolha um para saber mais sobre ele."
    
    # Menu com os botões para cada jogador
    menu_jogadores_cs = ReplyKeyboardMarkup(
        [
            [KeyboardButton("FalleN")],
            [KeyboardButton("KSCERATO")],
            [KeyboardButton("molodoy")],
            [KeyboardButton("YEKINDAR")],
            [KeyboardButton("yuurih")],
            [KeyboardButton("Treinador-sidde")],
            [KeyboardButton("Treinador-Hepa")],
            [KeyboardButton("🔙 Voltar ao menu principal")]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    # Envia a mensagem com os botões
    await bot.send_message(
        chat_id=chat_id,
        text=info_jogadores,
        reply_markup=menu_jogadores_cs
    )

async def handle_jogador_especifico(bot: Bot, chat_id: int, jogador: str):
    """
    Envia informações detalhadas sobre o jogador escolhido.
    """
    # Dicionário com informações sobre os jogadores
    
    info_jogadores = {
    "FalleN": """FalleN (Gabriel 'FalleN' Toledo) - Rifler 🎮
Idade: 32 anos 🎂
Origem: São Paulo, Brasil 🇧🇷
FalleN, conhecido como "O Capitão", é uma lenda do CS:GO, com anos de experiência e conquistas no cenário. Ele é um dos maiores nomes do Brasil e do mundo, reconhecido pela sua habilidade e liderança. Além de ser um rifler excepcional, é o capitão da equipe, guiando a FURIA com estratégias afiadas e um espírito vencedor. 🏆🔥
**Posição**: Rifler – O capitão da equipe, sempre comandando com sabedoria e ação! 💥🔝""",

    "Treinador-Hepa": """Hepa (Juan 'Hepa' Borges) - Treinador assistente 🧠
Idade: 28 anos 🎉
Origem: Espanha 🇪🇸
Hepa é o treinador assistente da FURIA, contribuindo com sua visão tática e conhecimento técnico para otimizar a preparação da equipe. Ele desempenha um papel fundamental no desenvolvimento de novos treinos e na análise do desempenho dos jogadores. 💪🔍
**Posição**: Treinador assistente – Ajudando a refinar cada detalhe para levar a FURIA ao topo! 🏅🔥""",

    "KSCERATO": """KSCERATO (Kaike 'KSCERATO' Cerato) - Rifler 🎯
Idade: 21 anos 🎂
Origem: Rio de Janeiro, Brasil 🇧🇷
KSCERATO é um dos principais responsáveis pelas jogadas de impacto na FURIA. Com uma grande habilidade de leitura de jogo e uma excelente pontaria, ele é essencial em momentos chave. Sua experiência em ler as movimentações dos adversários e executar jogadas de alto risco fazem dele uma peça-chave da equipe. 💥⚡
**Posição**: Rifler – Sempre à frente, pronto para decidir o jogo com sua precisão! ⚔️🔥""",

    "molodoy": """molodoy (Danil 'molodoy' Golubenko) - AWPer 🎯
Idade: 22 anos 🎉
Origem: Cazaquistão 🇰🇿
molodoy é o AWPer da equipe, e com sua precisão e domínio da AWP, ele é fundamental em jogos decisivos. Sua habilidade de ler o jogo e surpreender os adversários com suas jogadas de longo alcance fazem dele um dos principais responsáveis por desestabilizar os inimigos. 💣🔥
**Posição**: AWPer – Mestre dos tiros de longo alcance, sempre prontos para derrubar os adversários! 🔫💥""",

    "Treinador-sidde": """sidde (Sid Macedo) - Treinador 🎓
Idade: 30 anos 🎂
Origem: Brasil 🇧🇷
sidde é o treinador da equipe e responsável por guiar a FURIA nas análises de jogo, desenvolvimento tático e aprimoramento das habilidades dos jogadores. Sua experiência e visão estratégica fazem dele um dos pilares da equipe, trabalhando para maximizar o potencial de cada jogador. 🎯🧠
**Posição**: Treinador – A mente por trás das estratégias vencedoras da FURIA! 💡🔥""",

    "YEKINDAR": """YEKINDAR (Mareks 'YEKINDAR' Gaļinskis) - Rifler 🎯
Idade: 23 anos 🎂
Origem: Letônia 🇱🇻
YEKINDAR é um dos novos reforços da FURIA, trazendo sua experiência e habilidades de rifler agressivo. Ele é conhecido por sua movimentação rápida e leitura de jogo impecável, sendo uma peça essencial no controle do mapa e nas execuções de estratégias. 💥⚡
**Posição**: Rifler – Agilidade e precisão, sempre pronto para impactar no jogo! ⚡🔥""",

    "yuurih": """yuurih (Yuri Santos) - Rifler 🎯
Idade: 23 anos 🎉
Origem: Rio de Janeiro, Brasil 🇧🇷
Yuri Santos, ou yuurih, é um dos riflers mais habilidosos da FURIA. Com sua visão aguçada e habilidade de se posicionar estrategicamente, ele traz grande impacto nas partidas. Sua calma e precisão são essenciais para a equipe, especialmente em momentos decisivos. Uma verdadeira fera do CS:GO! 🔥🎮
**Posição**: Rifler – Líder da linha de frente, sempre com uma mira afiada! ⚔️🔥""",
}



    # Envia a mensagem sobre o jogador
    if jogador in info_jogadores:
        await bot.send_message(chat_id=chat_id, text=info_jogadores[jogador])
    
    # Após mostrar as informações, envia o menu novamente
    await handle_sobre_jogadores_cs(bot, chat_id)
