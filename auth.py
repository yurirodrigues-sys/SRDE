import sqlite3
from data_base import obter_conexao
from utils2 import validar_email,validar_senha

def registrar_usuario():
    print("\n--- CADASTRO ---")
    email = input("E-mail (nome.sobrenome@ufrpe.br): ").strip().lower()
    if not validar_email(email): print("Erro: Formato inválido!"); return
    senha = input("Senha (8+ números, sem consecutivos): ").strip()
    if not validar_senha(senha): print("Erro: Senha inválida."); return
    
    conn = obter_conexao()
    cursor = conn.cursor()
    try:
        # O uso de '?' previne SQL Injection
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
        conn.commit()
        print("Sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Este e-mail já está cadastrado.")
    finally:
        conn.close()

def recuperar_senha():
    print("\n--- RECUPERAÇÃO DE SENHA ---")
    email = input("E-mail institucional: ").strip().lower()
    
    conn = obter_conexao()
    cursor = conn.cursor()
    
    # Verifica se o usuário existe
    cursor.execute("SELECT email FROM usuarios WHERE email = ?", (email,))
    if not cursor.fetchone():
        print("E-mail não encontrado.")
        conn.close()
        return
        
    print("E-mail encontrado! Defina sua nova senha:")
    nova = input("Nova senha: ").strip()
    if validar_senha(nova):
        cursor.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (nova, email))
        conn.commit()
        print("Senha atualizada!")
    else:
        print("Erro: Senha inválida.")
    conn.close()

def deletar_conta():
    print("\n--- DELETAR CONTA ---")
    email = input("E-mail institucional: ").strip().lower()
    senha = input("Senha: ").strip()
    
    conn = obter_conexao()
    cursor = conn.cursor()
    
    # Verifica se a senha bate
    cursor.execute("SELECT email FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    if not cursor.fetchone():
        print("E-mail não encontrado ou senha incorreta.")
        conn.close()
        return
        
    confirmacao = input("Tem certeza que deseja deletar sua conta? (s/n): ").strip().lower()
    if confirmacao == 's':
        cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))
        conn.commit()
        print("Conta deletada com sucesso!")
    else:
        print("Operação cancelada.")
    conn.close()
