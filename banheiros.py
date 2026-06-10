from equipamentos import EquipamentoSanitario
from inventory import salvar_avaliacao
from utils import limpar_tela

BANHEIROS_INVENTARIO = {}

# --- CADASTRO AUTOMÁTICO DOS BANHEIROS ---
andares = ["TERREO", "1ANDAR", "2ANDAR", "3ANDAR"]
posicoes = {"E": "Esquerda", "M": "Meio", "D": "Direita"}

for andar in andares:
    nome_andar = "Térreo" if andar == "TERREO" else f"{andar[0]}º Andar"
    for sigla_pos, nome_pos in posicoes.items():
        id_pia = f"B_{andar}_PIA_{sigla_pos}"
        BANHEIROS_INVENTARIO[id_pia] = EquipamentoSanitario(id_pia, f"Pia {nome_pos} (Banheiro {nome_andar})", "Pia")
        
        id_vaso = f"B_{andar}_VASO_{sigla_pos}"
        BANHEIROS_INVENTARIO[id_vaso] = EquipamentoSanitario(id_vaso, f"Vaso {nome_pos} (Banheiro {nome_andar})", "Vaso Sanitário")


def executar_fluxo_avaliacao(alvo_id, nome_alvo):
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
    input("\nPressione Enter para continuar...")


def menu_banheiros():
    andares_opcoes = {
        "1": ("TERREO", "Térreo"),
        "2": ("1ANDAR", "1º Andar"),
        "3": ("2ANDAR", "2º Andar"),
        "4": ("3ANDAR", "3º Andar")
    }
    
    while True:
        limpar_tela()
        print("\n--- SELEÇÃO DE BANHEIRO ---")
        print("1. Banheiro Térreo")
        print("2. Banheiro 1º Andar")
        print("3. Banheiro 2º Andar")
        print("4. Banheiro 3º Andar")
        print("0. Voltar")
        
        opcao_andar = input("Escolha o andar: ").strip()
        if opcao_andar == "0":
            break
            
        if opcao_andar in andares_opcoes:
            andar_sigla, andar_nome = andares_opcoes[opcao_andar]
            
            while True:
                limpar_tela()
                print(f"\n=== EQUIPAMENTOS DO BANHEIRO: {andar_nome.upper()} ===")
                
                # Mapeia dinamicamente os objetos criados no dicionário local do módulo
                equipamentos = [
                    {"id": f"B_{andar_sigla}_PIA_E", "nome": "Pia Esquerda", "obj": BANHEIROS_INVENTARIO[f"B_{andar_sigla}_PIA_E"]},
                    {"id": f"B_{andar_sigla}_PIA_M", "nome": "Pia Meio", "obj": BANHEIROS_INVENTARIO[f"B_{andar_sigla}_PIA_M"]},
                    {"id": f"B_{andar_sigla}_PIA_D", "nome": "Pia Direita", "obj": BANHEIROS_INVENTARIO[f"B_{andar_sigla}_PIA_D"]},
                    {"id": f"B_{andar_sigla}_VASO_E", "nome": "Vaso Esquerdo", "obj": BANHEIROS_INVENTARIO[f"B_{andar_sigla}_VASO_E"]},
                    {"id": f"B_{andar_sigla}_VASO_M", "nome": "Vaso Meio", "obj": BANHEIROS_INVENTARIO[f"B_{andar_sigla}_VASO_M"]},
                    {"id": f"B_{andar_sigla}_VASO_D", "nome": "Vaso Direito", "obj": BANHEIROS_INVENTARIO[f"B_{andar_sigla}_VASO_D"]},
                ]
                
                print("Selecione qual deseja avaliar:")
                for idx, eq in enumerate(equipamentos, start=1):
                    status = eq["obj"].obter_status_atual()
                    print(f"{idx}. {eq['nome']} ({status})")
                print("0. Voltar")
                
                opcao_eq = input("Opção: ").strip()
                if opcao_eq == "0":
                    break
                    
                try:
                    idx_eq = int(opcao_eq) - 1
                    if 0 <= idx_eq < len(equipamentos):
                        escolhido = equipamentos[idx_eq]
                        executar_fluxo_avaliacao(escolhido["id"], f"{escolhido['nome']} do {andar_nome}")
                    else:
                        print("Opção inválida.")
                        input("\nPressione Enter para continuar...")
                except ValueError:
                    print("Opção inválida.")
                    input("\nPressione Enter para continuar...")
        else:
            print("Opção inválida.")
            input("\nPressione Enter para continuar...")
