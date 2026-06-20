from equipamentos import EquipamentoSanitario
from inventory2 import solicitar_avaliacao, exibir_historico_avaliacoes
from utils2 import limpar_tela
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

BANHEIROS_INVENTARIO = {}

andares = ["TERREO", "1ANDAR", "2ANDAR", "3ANDAR"]
posicoes = {"E": "Esquerda", "M": "Meio", "D": "Direita"}

for andar in andares:
    nome_andar = "Térreo" if andar == "TERREO" else f"{andar[0]}º Andar"
    for sigla_pos, nome_pos in posicoes.items():
        id_pia = f"B_{andar}_PIA_{sigla_pos}"
        BANHEIROS_INVENTARIO[id_pia] = EquipamentoSanitario(id_pia, f"Pia {nome_pos} (Banheiro {nome_andar})", "Pia")
        
        id_vaso = f"B_{andar}_VASO_{sigla_pos}"
        BANHEIROS_INVENTARIO[id_vaso] = EquipamentoSanitario(id_vaso, f"Vaso {nome_pos} (Banheiro {nome_andar})", "Vaso Sanitário")


def menu_banheiros(usuario_email="Desconhecido"):
    andares_opcoes = {
        "1": ("TERREO", "Térreo"),
        "2": ("1ANDAR", "1º Andar"),
        "3": ("2ANDAR", "2º Andar"),
        "4": ("3ANDAR", "3º Andar")
    }
    
    while True:
        limpar_tela()
        console.print(Panel("[bold cyan]=== VISTORIA: BANHEIROS DO PRÉDIO ===[/]", expand=False))
        print("1. Banheiro do Térreo")
        print("2. Banheiro do 1º Andar")
        print("3. Banheiro do 2º Andar")
        print("4. Banheiro do 3º Andar")
        print("0. Voltar")
        
        opcao_andar = input("\nSelecione o andar: ").strip()
        if opcao_andar == "0":
            break
            
        if opcao_andar in andares_opcoes:
            andar_chave, andar_nome = andares_opcoes[opcao_andar]
            
            while True:
                limpar_tela()
                console.print(Panel(f"[bold cyan]Banheiro - {andar_nome}[/]", expand=False))
                
                equipamentos = []
                for k, eq in BANHEIROS_INVENTARIO.items():
                    if f"B_{andar_chave}_" in k:
                        equipamentos.append({"id": k, "nome": eq.nome, "obj": eq})
                        
                tabela = Table(title=f"Itens do Banheiro ({andar_nome})")
                tabela.add_column("Nº", justify="center", style="bold")
                tabela.add_column("Equipamento")
                tabela.add_column("Último Status Registrado")
                
                for idx, eq in enumerate(equipamentos, start=1):
                    status_raw = eq["obj"].obter_status_atual()
                    if "Status: Bom" in status_raw:
                        status_colorido = f"[green]{status_raw}[/]"
                    elif "Status: Quebrado" in status_raw:
                        status_colorido = f"[red]{status_raw}[/]"
                    elif "Status: Desgastado" in status_raw:
                        status_colorido = f"[yellow]{status_raw}[/]"
                    else:
                        status_colorido = f"[white]{status_raw}[/]"
                        
                    tabela.add_row(str(idx), eq['nome'], status_colorido)
                
                console.print(tabela)
                console.print("\n[bold red]0.[/] Voltar")
                
                opcao_eq = input("\nSelecione qual deseja gerenciar: ").strip()
                if opcao_eq == "0":
                    break
                    
                try:
                    idx_eq = int(opcao_eq) - 1
                    if 0 <= idx_eq < len(equipamentos):
                        escolhido = equipamentos[idx_eq]
                        
                        while True:
                            limpar_tela()
                            console.print(Panel(f"[bold cyan]Gerenciamento:[/] {escolhido['nome']}\n[yellow]ID:[/] {escolhido['id']}", expand=False))
                            print("\n1. Registrar nova avaliação")
                            print("2. Visualizar Histórico completo de avaliações")
                            print("3. Voltar")
                            op_acao = input("\nOpção: ").strip()
                            
                            if op_acao == "3":
                                break
                            elif op_acao == "1":
                                limpar_tela()
                                solicitar_avaliacao(escolhido["id"], f"{escolhido['nome']}", usuario_email)
                                break
                            elif op_acao == "2":
                                limpar_tela()
                                exibir_historico_avaliacoes(escolhido["id"], escolhido["nome"])
                    else:
                        console.print("[bold red]Opção inválida.[/]")
                        input("\nPressione Enter para continuar...")
                except ValueError:
                    console.print("[bold red]Opção inválida.[/]")
                    input("\nPressione Enter para continuar...")
        else:
            console.print("[bold red]Opção inválida.[/]")
            input("\nPressione Enter para continuar...")
