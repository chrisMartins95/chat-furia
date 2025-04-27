# app/utils/ai_response.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar cliente da OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Cache simples em memória
response_cache = {}

def gerar_resposta_openai(message_text: str) -> str:
    # Primeiro, verifica se já temos a resposta salva
    if message_text in response_cache:
        print(f"🔁 Resposta do cache para: '{message_text}'")
        return response_cache[message_text]

    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um chatbot super fã da FURIA Esports, sempre com uma energia positiva "
                        "e vibrante! Responda de maneira empolgante e cheia de energia, como um verdadeiro "
                        "torcedor apaixonado de CS:GO."
                    )
                },
                {"role": "user", "content": message_text}
            ],
            temperature=0.8,
            max_tokens=150
        )
        reply_text = resposta.choices[0].message.content.strip()

        # Salva a resposta no cache
        response_cache[message_text] = reply_text

        return reply_text
    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        return "Opa, deu ruim aqui na minha cabeça gamer 😵. Tenta de novo aí!"
