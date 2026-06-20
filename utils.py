import re
import os
import hashlib

def limpar_tela():
    # 'cls' para Windows, 'clear' para Linux/Android (Pydroid)
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_email(email):
    return re.match(r"^[a-z]+\.[a-z]+@ufrpe\.br$", email) is not None

def validar_senha(senha):
    if len(senha) < 8 or not senha.isdigit(): return False
    
    for i in range(len(senha) - 1):
        if abs(int(senha[i+1]) - int(senha[i])) <= 1: return False
    return True
def gerar_hash(senha):
    """Gera um hash SHA-256 para a senha fornecida."""
    # O encode() transforma a string em bytes, exigência do hashlib
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()