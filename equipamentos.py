from inventory2 import obter_ultima_avaliacao

# Classe Base (Mãe): Contém tudo o que é comum a QUALQUER equipamento do prédio
class Equipamento:
    def __init__(self, id_item, nome, tipo):
        self.id = str(id_item)
        self.nome = nome
        self.tipo = tipo
        self.perifericos = []  # Por padrão, a maioria não tem periféricos

    def obter_status_atual(self):
        # Todos usam exatamente a mesma lógica de busca no banco
        return obter_ultima_avaliacao(self.id)


# Classe Filha: Especializada em eletrônicos
class Eletronico(Equipamento):
    def __init__(self, id_patrimonio, nome, tipo):
        # super().__init__ reaproveita o construtor da classe mãe
        super().__init__(id_patrimonio, nome, tipo)
        
        # Comportamento exclusivo do PC
        if tipo == "PC":
            self.perifericos = ["Monitor", "Mouse", "Teclado"]

    def obter_status_periferico(self, periferico):
        return obter_ultima_avaliacao(f"{self.id}_{periferico.lower()}")


# Classe Filha: Especializada em cadeiras
class Cadeira(Equipamento):
    def __init__(self, id_cadeira, nome):
        # Uma cadeira sempre terá o tipo "Cadeira"
        super().__init__(id_cadeira, nome, "Cadeira")


# Classe Filha: Especializada em itens de banheiro
class EquipamentoSanitario(Equipamento):
    def __init__(self, id_equipamento, nome, tipo):
        super().__init__(id_equipamento, nome, tipo)
