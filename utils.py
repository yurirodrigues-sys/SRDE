import re
import os

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