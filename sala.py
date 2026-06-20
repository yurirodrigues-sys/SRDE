from equipamentos import Eletronico, Cadeira
from inventory import solicitar_avaliacao, exibir_historico_avaliacoes
from utils import limpar_tela
from data_base import obter_conexao
from rich.console import Console
from rich.table import Table

console = Console()

def carregar_inventario_do_banco():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, tipo FROM equipamentos")
    linhas = cursor.fetchall()
    conn.close()
    
    inventario_atualizado = {}
    for id_item, nome, tipo in linhas:
        if tipo == "PC":
            inventario_atualizado[str(id_item)] = Eletronico(id_item, nome, tipo)
        elif tipo == "Cadeira":
            inventario_atualizado[str(id_item)] = Cadeira(id_item, nome)
        else:
            inventario_atualizado[str(id_item)] = Eletronico(id_item, nome, tipo)
    return inventario_atualizado

def menu_sala(eh_admin=False, usuario_email="Desconhecido"):
    while True:
        INVENTARIO = carregar_inventario_do_banco()
        limpar_tela()
        print("\n=== LABORATÓRIO 41 ===")
        
        if eh_admin:
            console.print("[bold yellow]⚙️ MODO ADMINISTRADOR ATIVO[/]")
            print("Comandos: Digite o ID para buscar | 'ADD' para cadastrar | 'DEL' para remover | '0' para voltar")
        else:
            print("Digite o ID do patrimônio (ou '0' para voltar)")
            
        id_busca = input("\nAção/ID: ").strip()
        
        if id_busca == "0":
            break
            
        if id_busca.upper() == "ADD" and eh_admin:
            limpar_tela()
            console.print("[bold green]=== CADASTRAR NOVO EQUIPAMENTO NO BANCO ===[/]\n")
            novo_id = input("Digite o novo ID de patrimônio: ").strip()
            
            if novo_id in INVENTARIO:
                console.print("\n[bold red]✗ Erro: Este ID já está cadastrado no banco de dados![/]")
            else:
                print("\nSelecione o tipo do item:")
                print("1. Computador (PC)\n2. Ar-condicionado\n3. Cadeira")
                tipo_op = input("Opção: ").strip()
                
                tipo_str = ""
                nome_item = ""
                
                if tipo_op == "1":
                    nome_item = input("Nome/Número do PC (Ex: Computador 26): ").strip()
                    tipo_str = "PC"
                elif tipo_op == "2":
                    nome_item = input("Nome do Ar (Ex: Ar-condicionado 4): ").strip()
                    tipo_str = "Ar"
                elif tipo_op == "3":
                    nome_item = input("Nome/Número da Cadeira (Ex: Cadeira 31): ").strip()
                    tipo_str = "Cadeira"
                
                if tipo_str:
                    conn = obter_conexao()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO equipamentos (id, nome, tipo) VALUES (?, ?, ?)", (novo_id, nome_item, tipo_str))
                    conn.commit()
                    conn.close()
                    console.print(f"\n[bold green]✓ {nome_item} gravado de forma permanente no SQLite![/]")
                else:
                    console.print("\n[bold red]✗ Opção inválida. Operação cancelada.[/]")
                    
            input("\nPressione Enter para continuar...")
            continue

        if id_busca.upper() == "DEL" and eh_admin:
            id_remover = input("Digite o ID do equipamento que deseja apagar definitivamente: ").strip()
            if id_remover in INVENTARIO:
                nome_removido = INVENTARIO[id_remover].nome
                
                conn = obter_conexao()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM equipamentos WHERE id = ?", (id_remover,))
                conn.commit()
                conn.close()
                
                console.print(f"\n[bold green]✓ {nome_removido} (ID: {id_remover}) foi deletado do banco de dados![/]")
            else:
                console.print("\n[bold red]✗ ID não encontrado no sistema.[/]")
            input("\nPressione Enter para continuar...")
            continue
        
        if id_busca in INVENTARIO:
            item = INVENTARIO[id_busca]
            
            while True:
                limpar_tela()
                tabela = Table(title=f"Monitoramento: {item.nome}", border_style="blue")
                tabela.add_column("Componente / Item", style="bold yellow")
                tabela.add_column("ID", justify="center", style="dim")
                tabela.add_column("Situação Atual")
                
                status_principal = item.obter_status_atual()
                if "Status: Bom" in status_principal: status_colorido = f"[green]{status_principal}[/]"
                elif "Status: Quebrado" in status_principal: status_colorido = f"[red]{status_principal}[/]"
                elif "Status: Desgastado" in status_principal: status_colorido = f"[yellow]{status_principal}[/]"
                else: status_colorido = f"[white]{status_principal}[/]"
                    
                tabela.add_row(item.nome, item.id, status_colorido)
                
                if item.perifericos:
                    for p in item.perifericos:
                        status_perf = item.obter_status_periferico(p)
                        if "Status: Bom" in status_perf: perf_colorido = f"[green]{status_perf}[/]"
                        elif "Status: Quebrado" in status_perf: perf_colorido = f"[red]{status_perf}[/]"
                        elif "Status: Desgastado" in status_perf: perf_colorido = f"[yellow]{status_perf}[/]"
                        else: perf_colorido = f"[white]{status_perf}[/]"
                            
                        tabela.add_row(f"  • {p}", f"{item.id}_{p.lower()}", perf_colorido)
                
                console.print(tabela)
                
                print("\nAções disponíveis:")
                print("1. Realizar uma nova avaliação")
                print("2. Visualizar Histórico de avaliações")
                print("3. Voltar ao menu anterior")
                opcao_acao = input("\nEscolha uma opção: ").strip()
                
                if opcao_acao == "3":
                    break
                    
                if opcao_acao in ["1", "2"]:
                    alvo_id = item.id
                    nome_alvo = item.nome
                    
                    if item.perifericos:
                        print("\nSelecione o componente de destino:")
                        print("1. Gabinete Principal\n2. Monitor\n3. Mouse\n4. Teclado")
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
                    
                    if opcao_acao == "1":
                        limpar_tela()
                        solicitar_avaliacao(alvo_id, nome_alvo, usuario_email)
                    elif opcao_acao == "2":
                        limpar_tela()
                        exibir_historico_avaliacoes(alvo_id, nome_alvo)
                else:
                    console.print("[bold red]Opção inválida![/]")
                    input("\nPressione Enter para continuar...")
        else:
            print("\n[Erro] Equipamento com este ID não foi encontrado no sistema.")
            input("Pressione Enter para continuar...")
