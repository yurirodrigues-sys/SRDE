from auth import registrar_usuario, recuperar_senha,deletar_conta
from sala import menu_sala
from data_base import inicializar_banco, obter_conexao
from utils import limpar_tela
from banheiros import menu_banheiros

def login():
            limpar_tela()
            email = input("E-mail: ").strip().lower()
            nome_usuario = email.split('.')[0]
            senha = input("Senha: ").strip()
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            usuario_valido = cursor.fetchone()
            conn.close()
            if usuario_valido:
                 while True:
                     limpar_tela()
                     print(f"\n=== Bem vindo a UniClasse {nome_usuario} ===")
                     print("1. Entrar no Laboratório 41\n2. Banheiros\n3. Logout")  
                     opcao = input("Opção: ").strip()
                     if opcao == "1":
                         menu_sala()
                     elif opcao == "2":
                         menu_banheiros()
                     elif opcao == "3":
                         break
                 return
            else:
                   print("Credenciais inválidas.")
                   
def main():
    inicializar_banco()
    while True:
        limpar_tela()
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