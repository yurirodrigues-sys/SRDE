import sqlite3

DB_NAME = "uniclasse.db"

def obter_conexao():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_NAME)

def inicializar_banco():
    """Cria as tabelas necessárias se elas não existirem."""
    conn = obter_conexao()
    cursor = conn.cursor()
    
    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            email TEXT PRIMARY KEY,
            senha TEXT NOT NULL
        )
    """)
    
    # Tabela de Inventário / Avaliações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            status TEXT NOT NULL,
            descricao TEXT DEFAULT 'N/A',
            data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
