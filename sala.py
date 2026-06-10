from equipamentos import Eletronico, Cadeira
from inventory import salvar_avaliacao
from utils import limpar_tela
INVENTARIO = {}

# Cadastrando os PCs fornecidos
ids_pcs = [
    20110, 20079, 20006, 20066, 20102, 20138, 20071, 18305, 20048, 20091,
    20003, 18856, 20034, 20090, 18854, 18861, 18839, 20151, 19996, 20119,
    20113, 20016, 18843, 20055, 20033
    ]

for i, id_pc in enumerate(ids_pcs, start=1):
    INVENTARIO[str(id_pc)] = Eletronico(id_pc, f"Computador {i:02d}", "PC")
    
# Cadastrando os Ar-condicionados fornecidos
ids_ares = [16024, 16025, 122148]
for i, id_ar in enumerate(ids_ares, start=1):
    INVENTARIO[str(id_ar)] = Eletronico(id_ar, f"Ar-condicionado {i}", "Ar")

ids_cadeiras = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
for i, id_cadeira in enumerate(ids_cadeiras, start=1):
    INVENTARIO[str(id_cadeira)] = Cadeira(id_cadeira, f"cadeira {i}")



def menu_sala():
    while True:
        limpar_tela()
        print("\n--- GERENCIAMENTO DE ELETRÔNICOS E MOBILIARIOS ---")
        print("Digite o ID do eletrônico para pesquisar ou '0' para voltar.")
        
        # Simulação da barra de pesquisa
        busca = input("Pesquisar ID: ").strip()
        
        if busca == "0":
            break
            
        # Verifica se o ID existe no inventário mapeado
        if busca in INVENTARIO:
            item = INVENTARIO[busca]
            print(f"\n[Sucesso] Item Encontrado!")
            print(f"Nome: {item.nome} | Tipo: {item.tipo} | ID: {item.id}")
            print(f"Última Avaliação Geral: {item.obter_status_atual()}")
            
            # Mostra o status dos periféricos se houver
            if item.perifericos:
                print("\n--- Situação dos Periféricos ---")
                for p in item.perifericos:
                    print(f"  > {p}: {item.obter_status_periferico(p)}")
            
            # Fluxo de avaliação usando o ID do objeto ou do periférico
            if input("\nDeseja realizar uma avaliação? (s/n): ").lower() == 's':
                alvo_id = item.id
                nome_alvo = item.nome
                
                # Se o item tiver periféricos, pergunta o que será avaliado
                if item.perifericos:
                    print("\nO que você deseja avaliar?")
                    print(f"1. O Computador (Gabinete principal)")
                    print(f"2. Monitor")
                    print(f"3. Mouse")
                    print(f"4. Teclado")
                    opcao_alvo = input("Opção: ").strip()
                    
                    if opcao_alvo == "2":
                        alvo_id = f"{item.id}_monitor"
                        nome_alvo = f"Monitor do {item.nome}"
                    elif opcao_alvo == "3":
                        alvo_id = f"{item.id}_mouse"
                        nome_alvo = f"Mouse do {item.nome}"
                    elif opcao_alvo == "4":
                        alvo_id = f"{item.id}_teclado"
                        nome_alvo = f"Teclado do {item.nome}"
                
                print(f"\nDefina o estado de: {nome_alvo}")
                print("1. Bom | 2. Desgastado | 3. Quebrado")
                aval = input("Status: ")
                
                if aval == "1": 
                    salvar_avaliacao(alvo_id, "Bom")
                    print("Avaliação salva com sucesso!")
                elif aval == "2": 
                    desc = input("Descrição do desgaste: ")
                    salvar_avaliacao(alvo_id, "Desgastado", desc)
                    print("Avaliação salva com sucesso!")
                elif aval == "3": 
                    salvar_avaliacao(alvo_id, "Quebrado")
                    print("Avaliação salva com sucesso!")
                else:
                    print("Opção de status inválida.")
        else:
            print("\n[Erro] Equipamento com este ID não foi encontrado no sistema.")
       
