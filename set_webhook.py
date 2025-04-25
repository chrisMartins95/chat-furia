import requests

TOKEN = "7679241514:AAEcLXmiBoLNqriflJ9BCnWc3OOCFDane_w"  # Substitua pelo token novo
URL_NGROK = "https://a75f-2804-5408-16-8c00-4dd3-ba5f-aec6-62c9.ngrok-free.app"  # Substitua pela URL HTTPS do ngrok

set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
data = {"url": f"{URL_NGROK}/webhook"}

response = requests.post(set_webhook_url, data=data)

print("Status:", response.status_code)
print("Resposta:", response.json())
