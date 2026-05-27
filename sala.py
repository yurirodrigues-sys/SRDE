from inventory2 import salvar_avaliacao, obter_ultima_avaliacao

def menu_sala():
    while True:
        print("\n--- SALA 1 ---")
        print("21. Ar-condicionado 1 | 22. Ar-condicionado 2")
        for i in range(1, 21): print(f"[{i:02d}] Computador {i}")
        print("[0] Voltar")

        escolha = input("\nEscolha: ")
        if escolha == "0": break

        if escolha == "21": item = "Ar-condicionado 1"
        elif escolha == "22": item = "Ar-condicionado 2"
        elif escolha.isdigit() and 1 <= int(escolha) <= 20: item = f"Computador {escolha}"
        else: continue

        print(f"\n> {item} | Última: {obter_ultima_avaliacao(item)}")
        if input("Deseja avaliar? (s/n): ").lower() == 's':
            print("1. Bom | 2. Desgastado | 3. Quebrado")
            aval = input("Status: ")
            if aval == "1": salvar_avaliacao(item, "Bom")
            elif aval == "2": salvar_avaliacao(item, "Desgastado", input("Descrição: "))
            elif aval == "3": salvar_avaliacao(item, "Quebrado")