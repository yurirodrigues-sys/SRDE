import os

ARQUIVO = "inventario.txt"

def salvar_avaliacao(item, status, desc="N/A"):
    with open(ARQUIVO, "a") as f:
        f.write(f"Item: {item} | Status: {status} | Obs: {desc}\n")

def obter_ultima_avaliacao(item):
    if not os.path.exists(ARQUIVO): return "Nenhuma avaliação registrada."
    with open(ARQUIVO, "r") as f:
        historico = [l.strip() for l in f if f"Item: {item}" in l]
    return historico[-1] if historico else "Nenhuma avaliação registrada."
