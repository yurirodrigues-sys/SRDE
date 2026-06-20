import csv
from datetime import datetime
from auth2 import registrar_usuario, recuperar_senha, deletar_conta, deletar_conta_admin
from sala2 import menu_sala
from data_base import inicializar_banco, obter_conexao
from utils2 import limpar_tela, gerar_hash
from banheiros import menu_banheiros
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def dashboard_critico():
    limpar_tela()
    console.print(Panel("[bold red]=== DASHBOARD DE ITENS CRÍTICOS ===[/]", border_style="red", expand=False))
    
    conn = obter_conexao()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT item, status, descricao, usuario_email, data_avaliacao 
        FROM avaliacoes a
        WHERE id = (SELECT MAX(id) FROM avaliacoes WHERE item = a.item)
        AND status IN ('Quebrado', 'Desgastado')
        ORDER BY data_avaliacao DESC
    """)
    itens_criticos = cursor.fetchall()
    conn.close()
    
    if not itens_criticos:
        console.print("\n[bold green]✓ Excelente! Nenhum equipamento está quebrado ou desgastado no momento.[/]")
    else:
        tabela = Table(title="Equipamentos Precisando de Manutenção Urgente")
        tabela.add_column("ID do Item", style="bold cyan")
        tabela.add_column("Status", justify="center")
        tabela.add_column("Reportado Por", style="magenta")
        tabela.add_column("Descrição/Obs")
        tabela.add_column("Data da Avaliação", justify="right", style="dim")
        
        for item, status, desc, email, data in itens_criticos:
            cor_status = "[bold red]" if status == "Quebrado" else "[bold yellow]"
            tabela.add_row(item, f"{cor_status}{status}[/]", email, desc, data)
            
        console.print(tabela)
        
    input("\nPressione Enter para voltar ao menu...")


def exportar_relatorios_csv():
    """Item 5: Extrai os dados do SQLite e gera ficheiros CSV compatíveis com o Excel."""
    limpar_tela()
    console.print(Panel("[bold green]📊 CENTRAL DE EXPORTAÇÃO DE RELATÓRIOS (CSV/EXCEL)[/]", border_style="green", expand=False))
    print("1. Exportar Histórico Completo de Vistorias/Avaliações")
    print("2. Exportar Apenas Diagnósticos de Itens Críticos (Manutenção)")
    print("0. Voltar")
    
    opcao = input("\nEscolha o relatório que deseja gerar: ").strip()
    if opcao == "0":
        return
        
    conn = obter_conexao()
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if opcao == "1":
        cursor.execute("""
            SELECT id, item, status, descricao, usuario_email, data_avaliacao 
            FROM avaliacoes 
            ORDER BY data_avaliacao DESC
        """)
        dados = cursor.fetchall()
        colunas = ["ID_Avaliacao", "ID_Item_Equipamento", "Status_Estado", "Descricao_Observacao", "Email_Avaliador", "Data_Hora_Vistoria"]
        nome_arquivo = f"historico_completo_vistorias_{timestamp}.csv"
        titulo_sucesso = "Histórico Completo"
        
    elif opcao == "2":
        cursor.execute("""
            SELECT item, status, descricao, usuario_email, data_avaliacao 
            FROM avaliacoes a
            WHERE id = (SELECT MAX(id) FROM avaliacoes WHERE item = a.item)
            AND status IN ('Quebrado', 'Desgastado')
            ORDER BY data_avaliacao DESC
        """)
        dados = cursor.fetchall()
        colunas = ["ID_Item_Equipamento", "Status_Critico", "Descricao_Defeito", "Email_Avaliador", "Data_Hora_Registro"]
        nome_arquivo = f"relatorio_itens_criticos_{timestamp}.csv"
        titulo_sucesso = "Itens Críticos de Manutenção"
        
    else:
        console.print("\n[bold red]✗ Opção inválida! Operação cancelada.[/]")
        conn.close()
        input("\nPressione Enter para continuar...")
        return

    if not dados:
        console.print("\n[bold yellow]⚠️ Não foram encontrados registos no banco de dados para gerar este relatório no momento.[/]")
        conn.close()
        input("\nPressione Enter para continuar...")
        return

    try:
        # 'utf-8-sig' escreve o BOM (Byte Order Mark) para que o Excel em Português abra com acentos corretos
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as ficheiro_csv:
            escritor = csv.writer(ficheiro_csv, delimiter=";") # Ponto e vírgula separa as colunas nativamente no Excel
            
            # Escreve o cabeçalho das colunas
            escritor.writerow(colunas)
            # Escreve todas as linhas de dados vindas do banco
            escritor.writerows(dados)
            
        console.print(f"\n[bold green]✓ Sucesso! O Relatório de '{titulo_sucesso}' foi gerado com êxito.[/]")
        console.print(f"[bold]Ficheiro salvo em:[/] [yellow]{nome_arquivo}[/]")
    except Exception as e:
        console.print(f"\n[bold red]✗ Erro crítico ao tentar gravar o ficheiro CSV: {e}[/]")
        
    conn.close()
    input("\nPressione Enter para continuar...")


def login():
    limpar_tela()
    console.print("[bold magenta]=== LOGIN UNICLASSE ===[/]\n")
    email = input("E-mail: ").strip().lower()
    nome_usuario = email.split('.')[0].capitalize()
    senha = input("Senha: ").strip()
    senha_hash = gerar_hash(senha)
    
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT email, tipo FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
    usuario_valido = cursor.fetchone()
    conn.close()
    
    if usuario_valido:
        email_logado, tipo_usuario = usuario_valido
        eh_admin = (tipo_usuario == 'admin')
        
        while True:
            limpar_tela()
            
            if eh_admin:
                console.print(Panel(f"[bold gold1]💻 PAINEL DO ADMINISTRADOR[/]\n[bold]Bem-vindo, {nome_usuario} (Gestão Geral)[/]", title="UniClasse", border_style="yellow"))
                print("\n1. Ver Dashboard de Itens Críticos (Manutenção)")
                print("2. Gerenciar Laboratório 41 (Buscar / Adicionar / Remover)")
                print("3. Gerenciar Banheiros (Visualizar)")
                print("4. Excluir Contas de Alunos (Moderação)")
                print("5. Exportar Dados para CSV/Excel (Relatórios)")
                print("6. Logout")
            else:
                console.print(Panel(f"[bold green]✓[/] Login efetuado com sucesso!\n[bold]Bem-vindo, {nome_usuario}![/]", title="UniClasse", border_style="green"))
                print("\n1. Vistoria: Laboratório 41")
                print("2. Vistoria: Banheiros")
                print("3. Logout")  
            
            opcao = input("\nOpção: ").strip()
            
            if eh_admin:
                if opcao == "1":
                    dashboard_critico()
                elif opcao == "2":
                    menu_sala(eh_admin=True, usuario_email=email_logado)
                elif opcao == "3":
                    menu_banheiros(usuario_email=email_logado)
                elif opcao == "4":
                    deletar_conta_admin()
                    input("\nPressione Enter para continuar...")
                elif opcao == "5":
                    exportar_relatorios_csv()
                elif opcao == "6":
                    break
            else:
                if opcao == "1":
                    menu_sala(eh_admin=False, usuario_email=email_logado)
                elif opcao == "2":
                    menu_banheiros(usuario_email=email_logado)
                elif opcao == "3":
                    break
        return
    else:
        console.print("\n[bold red]✗ Credenciais inválidas. Verifique seu e-mail e senha.[/]")
        input("\nPressione Enter para voltar...")
           
def main():
    inicializar_banco()
    while True:
        limpar_tela()
        console.print(Panel(f"\n[bold yellow]=== UniClasse ===\nDesenvolvido para Fiscalização de Infraestrutura"))
        console.print(Panel(f"1. Login\n2. Cadastrar Novo Utilizador\n3. Recuperar Senha\n4. Sair do Programa\n5. Deletar Minha Conta (Autoexclusão)"))
        op = input("Opção: ")
        if op == "1": login()
        elif op == "2": registrar_usuario()
        elif op == "3": recuperar_senha()
        elif op == "4": break
        elif op == "5": deletar_conta()

if __name__ == "__main__":
    main()
