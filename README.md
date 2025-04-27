
# 🐯 FURIA Chatbot 🕹️

Seja bem-vindo ao **FURIA Chatbot**! 🚀 Um projeto desenvolvido para interagir com os torcedores da **FURIA Esports** no Telegram! O bot é personalizado para fãs de CS:GO e traz informações sobre a equipe, seus jogadores e muito mais!

## ⚡ O que é isso?

Este projeto é um chatbot interativo no **Telegram**, desenvolvido para fornecer informações sobre a **FURIA Esports**, seus jogadores e equipe. A ideia é criar uma experiência de interação divertida e informativa para os fãs da FURIA!

## 🔥 Funcionalidades

- **Coleta de Dados**: O bot coleta dados do usuário, como nome, idade, cidade e nick de jogos para personalizar a experiência. 
- **Menus Interativos**: Envia menus dinâmicos com várias opções, como informações sobre a FURIA, o time de CS, e os jogadores.
- **Informações sobre a FURIA**: O bot compartilha a história da organização e seu impacto no cenário de esports.
- **Time de CS**: Fornece detalhes sobre os jogadores do time de CS:GO da FURIA, incluindo posições e informações interessantes sobre cada um.
- **Respostas Inteligentes**: Utiliza uma abordagem de NLP (Natural Language Processing) para fornecer respostas personalizadas baseadas nas interações do usuário.

## 🛠️ Tecnologias

- **FastAPI**: Framework para criar a API e gerenciar a interação com o Telegram.
- **python-telegram-bot**: Biblioteca para interagir com a API do Telegram.
- **SQLite**: Banco de dados para armazenar informações dos usuários.
- **Pydantic**: Para validação de dados e modelos de dados robustos.
- **dotenv**: Para carregar variáveis de ambiente de maneira segura.
- **OpenAI** (opcional): Integrado para fornecer respostas dinâmicas (mas você está fazendo isso manualmente no projeto agora).

## ⚙️ Como Rodar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/furia-chatbot.git
   cd furia-chatbot
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` e adicione as seguintes variáveis:
   ```bash
   TELEGRAM_TOKEN=seu_token_do_telegram
   OPENAI_API_KEY=sua_chave_openai
   ```

4. Rode o servidor FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

5. Configure o webhook no Telegram para a URL da sua API (requer um servidor em produção ou uso de ferramentas como o ngrok para desenvolvimento local).

## 📲 Testando

Após rodar o bot, envie mensagens para ele no Telegram e comece a interagir! O bot irá perguntar seu nome, idade, cidade e nick de jogos, e depois fornecer opções como:

- 🐱‍👤 Quem é a FURIA?
- 🎮 Falar sobre os jogadores
- 🔙 Voltar ao menu principal

## 🤖 Contribuindo

Sinta-se à vontade para fazer contribuições! Se você tiver ideias ou melhorias, basta criar uma **issue** ou enviar um **pull request**.

## 🚀 Melhorias Futuras

- Adicionar integração com outras plataformas de mídia social da FURIA.
- Melhorar a parte de NLP para respostas mais dinâmicas e naturais.
- Expandir o banco de dados com mais informações sobre a equipe e torcedores.

