FROM python:3.12-slim

# Instala dependências de sistema necessárias para a instalação de pacotes Python com dependências nativas
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*  # Limpa o cache do apt para reduzir a imagem

WORKDIR /app

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte
COPY . .

# Expõe a porta em que o servidor será executado
EXPOSE 8000

# Comando para rodar o servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
