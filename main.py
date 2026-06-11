from auth import registrar_usuario, recuperar_senha,deletar_conta
from sala import menu_sala
import os

def login():
    if not os.path.exists("usuarios.txt"): print("Sem usuários."); return
    email = input("E-mail: ").strip().lower()
    # split do email para aparecer so a primeira palavra
    nome_usuario = email.split('.')[0]
    
    senha = input("Senha: ").strip()
    with open("usuarios.txt", "r") as f:
        for linha in f:
            u, s = linha.strip().split('=')
            if u == email and s == senha:
                while True:
                    print(f"\n=== Bem vindo a UniClasse {nome_usuario} ===")
                    print("1. Entrar no Laboratório 41\n2. logout")
                    if input("Opção: ") == "1": menu_sala()
                   
                    else: break
                return
    print("Credenciais inválidas.")

def main():
    while True:
        print("\n=== UniClasse ===")
        print("1. Login\n2. Cadastrar\n3. Recuperar senha\n4. Sair\n5. deletar")
        op = input("Opção: ")
        if op == "1": login()
        elif op == "2": registrar_usuario()
        elif op == "3": recuperar_senha()
        elif op == "4": break
        elif op == "5": deletar_conta()

if __name__ == "__main__":
    main()