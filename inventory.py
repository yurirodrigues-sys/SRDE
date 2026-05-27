from data_base import obter_conexao

def salvar_avaliacao(item, status, desc="N/A"):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO avaliacoes (item, status, descricao) VALUES (?, ?, ?)", 
        (item, status, desc)
    )
    conn.commit()
    conn.close()

def obter_ultima_avaliacao(item):
    conn = obter_conexao()
    cursor = conn.cursor()
    # Busca a avaliação mais recente baseada no ID gerado automaticamente
    cursor.execute(
        "SELECT status, descricao FROM avaliacoes WHERE item = ? ORDER BY id DESC LIMIT 1", 
        (item,)
    )
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        status, desc = resultado
        return f"Status: {status} | Obs: {desc}"
    return "Nenhuma avaliação registrada."
