from data_base import obter_conexao
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def salvar_avaliacao(item, status, desc="N/A", usuario_email="Desconhecido"):
    """Insere a nova linha no banco de dados gravando quem efetuou a vistoria."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO avaliacoes (item, status, descricao, usuario_email) VALUES (?, ?, ?, ?)", 
        (item, status, desc, usuario_email)
    )
    conn.commit()
    conn.close()

def obter_ultima_avaliacao(item):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status, descricao, usuario_email FROM avaliacoes WHERE item = ? ORDER BY id DESC LIMIT 1", 
        (item,)
    )
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        status, desc, email = resultado
        return f"Status: {status} | Obs: {desc} | Por: {email}"
    return "Nenhuma avaliação registrada."

def exibir_historico_avaliacoes(item_id, nome_item):
    """Busca todas as avaliações de um ID e exibe a evolução temporal e quem avaliou."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status, descricao, usuario_email, data_avaliacao FROM avaliacoes WHERE item = ? ORDER BY data_avaliacao DESC", 
        (item_id,)
    )
    historico = cursor.fetchall()
    conn.close()
    
    console.print(Panel(f"[bold blue]📜 Histórico de Evolução de Estado[/]\n[yellow]Item:[/] {nome_item} (ID: {item_id})", expand=False))
    
    if not historico:
        console.print("\n[bold yellow]⚠️ Nenhuma avaliação anterior foi encontrada para este item.[/]")
    else:
        tabela = Table(title=f"Evolução Temporal - {nome_item}")
        tabela.add_column("Data e Hora", justify="center", style="dim")
        tabela.add_column("Situação/Status", justify="center")
        tabela.add_column("Avaliador (Log)", style="cyan")
        tabela.add_column("Observações / Justificativa")
        
        for status, desc, email, data in historico:
            if status == "Bom":
                cor = "[bold green]"
            elif status == "Desgastado":
                cor = "[bold yellow]"
            else:
                cor = "[bold red]"
                
            tabela.add_row(data, f"{cor}{status}[/]", email, desc)
            
        console.print(tabela)
        
    input("\nPressione Enter para continuar...")

def solicitar_avaliacao(alvo_id, nome_alvo, usuario_email):
    """Realiza a coleta dos dados enviando o e-mail capturado na sessão atual."""
    console.print(Panel(f"[bold blue]Avaliação de Infraestrutura[/]\n[yellow]Item:[/] {nome_alvo}", expand=False))
    
    console.print("\n[bold]Selecione o estado atual do item:[/]")
    console.print("  [bold green]1.[/] Bom")
    console.print("  [bold yellow]2.[/] Desgastado")
    console.print("  [bold red]3.[/] Quebrado")
    
    aval = input("\nStatus: ").strip()
    
    if aval == "1": 
        salvar_avaliacao(alvo_id, "Bom", usuario_email=usuario_email)
        console.print("\n[bold green]✓ Avaliação salva com sucesso![/]")
    elif aval == "2": 
        desc = input("Descrição do desgaste: ").strip()
        salvar_avaliacao(alvo_id, "Desgastado", desc, usuario_email=usuario_email)
        console.print("\n[bold green]✓ Avaliação salva com sucesso![/]")
    elif aval == "3": 
        desc = input("Descrição do defeito/quebra: ").strip()
        salvar_avaliacao(alvo_id, "Quebrado", desc, usuario_email=usuario_email)
        console.print("\n[bold green]✓ Avaliação salva com sucesso![/]")
    else:
        console.print("\n[bold red]Opção inválida![/]")
        
    input("\nPressione Enter para continuar...")
