class Pergunta:
    def __init__(self, data, alternativas, dicas):
        self.id_pergunta = data['id_pergunta']
        self.enunciado = data['enunciado']
        self.id_nivel = data['id_nivel']
        self.alternativas = alternativas
        self.dicas = dicas

    def exibir_pergunta(self):
        letras = ['A', 'B', 'C', 'D']
        print(f"\n{self.enunciado}")
        for i in range(len(self.alternativas)):
            print(f"{letras[i]} - {self.alternativas[i]['texto']}")
        print("\nDigite 'DICA' para receber uma dica")

    def alternativa_correta(self):
        for i in range(len(self.alternativas)):
            if self.alternativas[i]['correta'] == 1:
                return self.alternativas[i]
        return None

    def alternativa_por_letra(self, letra):
        letras = ['A', 'B', 'C', 'D']
        letra = letra.upper()
        if letra in letras:
            idx = letras.index(letra)
            if idx < len(self.alternativas):
                return self.alternativas[idx]
        return None
