import requests  # Importa a biblioteca requests para fazer requisições HTTP

# Define o token do seu bot do Telegram (substitua pelo seu token pessoal)
TOKEN = "7808482091:AAGCW7FlKrh_eXgWHRKKADDCRJJtKpW1R70"  

# URL do ngrok, que é usada para expor a aplicação local via túnel (substitua pela URL gerada pelo ngrok)
URL_NGROK = "https://d467-2804-5408-16-8c00-10f9-704-a20a-89a8.ngrok-free.app"

# URL da API do Telegram para configurar o webhook do bot
set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"

# Dados que serão enviados na requisição para configurar o webhook (a URL do ngrok + o endpoint /webhook)
data = {"url": f"{URL_NGROK}/webhook"}

# Realiza uma requisição POST para a API do Telegram para configurar o webhook
response = requests.post(set_webhook_url, data=data)

# Exibe o status da requisição (200 significa sucesso)
print("Status:", response.status_code)

# Exibe a resposta JSON da requisição para ver os detalhes do resultado
print("Resposta:", response.json())
