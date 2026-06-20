import sqlite3
from data_base import obter_conexao
from utils2 import validar_email, validar_senha, gerar_hash
from rich.panel import Panel
from rich.console import Console

console = Console()

def registrar_usuario():
    console.print(Panel(f"\n--- CADASTRO ---"))
    email = input("E-mail (nome.sobrenome@ufrpe.br): ").strip().lower()
    if not validar_email(email): print("Erro: Formato inválido!"); return
    senha = input("Senha (8+ números, sem consecutivos): ").strip()
    if not validar_senha(senha): print("Erro: Senha inválida."); return
    
    conn = obter_conexao()
    cursor = conn.cursor()
    try:
        senha_hash = gerar_hash(senha)
        # Força o tipo como 'aluno' por padrão em novos cadastros externos
        cursor.execute("INSERT INTO usuarios (email, senha, tipo) VALUES (?, ?, 'aluno')", (email, senha_hash))
        conn.commit()
        print("Sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Este e-mail já está cadastrado.")
    finally:
        conn.close()

def recuperar_senha():
    console.print(Panel(f"\n--- RECUPERAÇÃO DE SENHA ---"))
    email = input("E-mail institucional: ").strip().lower()
    
    conn = obter_conexao()
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM usuarios WHERE email = ?", (email,))
    if not cursor.fetchone():
        print("E-mail não encontrado.")
        conn.close()
        return
        
    print("E-mail encontrado! Defina sua nova senha:")
    nova = input("Nova senha: ").strip()
    if validar_senha(nova):
        nova_hash = gerar_hash(nova)
        cursor.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (nova_hash, email))
        conn.commit()
        print("Senha updated!")
    else:
        print("Erro: Senha inválida.")
    conn.close()

def deletar_conta():
    console.print(Panel(f"\n--- DELETAR MINHA PRÓPRIA CONTA ---"))
    email = input("E-mail institucional: ").strip().lower()
    senha = input("Senha: ").strip()
    
    senha_hash = gerar_hash(senha)
    conn = obter_conexao()
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
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

def deletar_conta_admin():
    """Função exclusiva do menu administrativo para expurgar contas do banco."""
    console.print(Panel(f"\n--- ADMIN: EXCLUIR CONTA DE USUÁRIO ---", border_style="red"))
    email_alvo = input("Digite o e-mail completo do aluno a ser removido: ").strip().lower()
    
    conn = obter_conexao()
    cursor = conn.cursor()
    
    cursor.execute("SELECT email, tipo FROM usuarios WHERE email = ?", (email_alvo,))
    resultado = cursor.fetchone()
    
    if not resultado:
        console.print("[bold red]Erro: Usuário não encontrado no sistema.[/]")
        conn.close()
        return
        
    _, tipo = resultado
    if tipo == 'admin':
        console.print("[bold red]Erro de permissão: Um administrador não pode deletar outro administrador por aqui.[/]")
        conn.close()
        return
        
    confirmacao = input(f"Tem certeza que deseja DELETAR PERMANENTEMENTE o usuário {email_alvo}? (s/n): ").strip().lower()
    if confirmacao == 's':
        cursor.execute("DELETE FROM usuarios WHERE email = ?", (email_alvo,))
        conn.commit()
        console.print("[bold green]✓ Conta de usuário removida do banco de dados com sucesso![/]")
    else:
        print("Operação cancelada.")
    conn.close()
