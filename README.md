Aqui está uma versão ajustada do seu `README.md` com as melhorias necessárias:

---

# 🐯 FURIA Chatbot 🕹️

Seja bem-vindo ao **FURIA Chatbot**! 🚀 Um projeto desenvolvido para interagir com os torcedores da **FURIA Esports** no Telegram. O bot é personalizado para fãs de **CS2** e traz informações sobre a equipe, seus jogadores e muito mais!

## ⚡ O que é isso?

Este projeto é um chatbot interativo no **Telegram**, desenvolvido para fornecer informações sobre a **FURIA Esports**, seus jogadores e equipe. A ideia é criar uma experiência de interação divertida e informativa para os fãs da FURIA.

## 🔥 Funcionalidades

* **Coleta de Dados**: O bot coleta dados do usuário, como nome, idade, cidade e nick de jogos para personalizar a experiência.
* **Menus Interativos**: Envia menus dinâmicos com várias opções, como informações sobre a FURIA, o time de CS e os jogadores.
* **Loja MTBda FURIA**: Oferece informações sobre a loja oficial da FURIA, permitindo que os torcedores conheçam os produtos e façam compras diretamente pelo bot.
* **Informações sobre a FURIA**: O bot compartilha a história da organização e seu impacto no cenário de esports.
* **Time de CS**: Fornece detalhes sobre os jogadores do time de **CS\:GO** da FURIA, incluindo posições e informações interessantes sobre cada um.
* **Hype News**: Últimas notícias sobre a FURIA e o cenário de esports.
* **Respostas Inteligentes**: Oferece respostas personalizadas com base nas interações do usuário.

## 🛠️ Tecnologias

* **FastAPI**: Framework para criar a API e gerenciar a interação com o Telegram.
* **python-telegram-bot**: Biblioteca para interagir com a API do Telegram.
* **SQLite**: Banco de dados para armazenar informações dos usuários.
* **Pydantic**: Para validação de dados e modelos de dados robustos.
* **dotenv**: Para carregar variáveis de ambiente de maneira segura.

## ⚙️ Como Rodar

### Pré-requisitos

Certifique-se de ter o Python 3.8 ou superior instalado.

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
   DATABASE_URL=sqlite:///db.sqlite3
   ```

4. Rode o servidor FastAPI:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Configure o webhook no Telegram para a URL da sua API (requer um servidor em produção ou o uso de ferramentas como o **ngrok** para desenvolvimento local).

## 📲 Testando

Após rodar o bot, envie mensagens para ele no Telegram e comece a interagir! O bot irá perguntar seu nome, idade, cidade e nick de jogos, e depois fornecerá opções como:

* 🐱‍👤 Quem é a FURIA?
* 🎮 Falar sobre os jogadores
* 🔙 Voltar ao menu principal
* 🔥 Últimas notícias

## 🤖 Contribuindo

Sinta-se à vontade para fazer contribuições! Se você tiver ideias ou melhorias, basta criar uma **issue** ou enviar um **pull request**.

## 🚀 Melhorias Futuras

* Adicionar integração com outras plataformas de mídia social da FURIA.
* Melhorar a parte de NLP para respostas mais dinâmicas e naturais.
* Expandir o banco de dados com mais informações sobre a equipe e torcedores.

---

Eu removi as partes relacionadas ao OpenAI, já que você está tratando das respostas manualmente, e também ajustei a parte de variáveis de ambiente para refletir as suas necessidades atuais.
