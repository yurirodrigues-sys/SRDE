import sqlite3
from utils import gerar_hash

DB_NAME = "uniclasse.db"

def obter_conexao():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB_NAME)

def inicializar_banco():
    """Cria as tabelas necessárias se elas não existirem e popula dados iniciais."""
    conn = obter_conexao()
    cursor = conn.cursor()
    
    # Tabela de Usuários (Item 4)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            email TEXT PRIMARY KEY,
            senha TEXT NOT NULL,
            tipo TEXT DEFAULT 'aluno'
        )
    """)
    
    # Tabela de Inventário / Avaliações atualizada com LOG de usuário (Item 3)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            status TEXT NOT NULL,
            descricao TEXT DEFAULT 'N/A',
            usuario_email TEXT DEFAULT 'Desconhecido',
            data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # MIGRAÇÃO SEGURA: Se o banco já existir localmente sem a coluna, adiciona sem quebrar os dados
    try:
        cursor.execute("ALTER TABLE avaliacoes ADD COLUMN usuario_email TEXT DEFAULT 'Desconhecido'")
    except sqlite3.OperationalError:
        pass  # A coluna já existe, ignora o erro
    
    # Nova tabela de Equipamentos para o cadastro dinâmico do Admin (Item 4)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipamentos (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)
    
    # SEED: Cria automaticamente o usuário Administrador solicitado se não existir (Item 4)
    admin_email = "admin.fiscal@ufrpe.br"
    cursor.execute("SELECT email FROM usuarios WHERE email = ?", (admin_email,))
    if not cursor.fetchone():
        senha_hash = gerar_hash("13579135")
        cursor.execute("INSERT INTO usuarios (email, senha, tipo) VALUES (?, ?, 'admin')", (admin_email, senha_hash))
        
    # SEED: Migra a lista inicial de equipamentos fixos se a tabela estiver vazia (Item 4)
    cursor.execute("SELECT COUNT(*) FROM equipamentos")
    if cursor.fetchone()[0] == 0:
        ids_pcs = [
            20110, 20079, 20006, 20066, 20102, 20138, 20071, 18305, 20048, 20091,
            20003, 18856, 20034, 20090, 18854, 18861, 18839, 20151, 19996, 20119,
            20113, 20016, 18843, 20055, 20033
        ]
        for i, id_pc in enumerate(ids_pcs, start=1):
            cursor.execute("INSERT INTO equipamentos (id, nome, tipo) VALUES (?, ?, 'PC')", (str(id_pc), f"Computador {i:02d}"))
            
        ids_ares = [16024, 16025, 122148]
        for i, id_ar in enumerate(ids_ares, start=1):
            cursor.execute("INSERT INTO equipamentos (id, nome, tipo) VALUES (?, ?, 'Ar')", (str(id_ar), f"Ar-condicionado {i}"))

        for id_cadeira in range(1, 31):
            cursor.execute("INSERT INTO equipamentos (id, nome, tipo) VALUES (?, ?, 'Cadeira')", (str(id_cadeira), f"Cadeira {id_cadeira:02d}"))
            
    conn.commit()
    conn.close()
