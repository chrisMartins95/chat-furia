import sqlite3

# Função para criar o banco de dados e a tabela de mensagens
def create_db():
    # Conecta ao banco de dados (ou cria, se não existir)
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # Cria a tabela "messages" se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            user_id INTEGER, 
            message TEXT,  
            response TEXT, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  
        )
    ''')

    # Confirma as mudanças no banco
    conn.commit()
    # Fecha a conexão
    conn.close()

# Função para salvar uma mensagem e a resposta no banco de dados
def save_message(user_id: int, message: str, response: str):
    # Conecta ao banco de dados
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # Insere uma nova mensagem e resposta na tabela "messages"
    cursor.execute('''
        INSERT INTO messages (user_id, message, response)
        VALUES (?, ?, ?)
    ''', (user_id, message, response))  # Substitui os "?" pelos valores passados

    # Confirma a inserção no banco
    conn.commit()
    # Fecha a conexão
    conn.close()
