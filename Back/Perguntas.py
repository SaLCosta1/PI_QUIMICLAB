class Pergunta:
    def __init__(self, data, alternativas, dicas):
        self.id_pergunta = data["id_pergunta"]
        self.enunciado = data["enunciado"]
        self.id_nivel = data["id_nivel"]
        self.imagem = data.get("imagem")
        self.imagem_mime = data.get("imagem_mime")
        self.alternativas = alternativas
        self.dicas = dicas

    def tem_imagem(self) -> bool:
        return bool(self.imagem)

    def exibir_pergunta(self):
        letras = ["A", "B", "C", "D"]
        print(f"\n{self.enunciado}")
        for i in range(len(self.alternativas)):
            print(f"{letras[i]} - {self.alternativas[i]['texto']}")
        print("\nDigite DICA para receber uma dica")

    def alternativa_correta(self):
        for alt in self.alternativas:
            if alt["correta"] == 1:
                return alt
        return None

    def alternativa_por_letra(self, letra):
        letras = ["A", "B", "C", "D"]
        letra = letra.upper()
        for i in range(len(letras)):
            if letras[i] == letra:
                if i < len(self.alternativas):
                    return self.alternativas[i]
                return None
        return None
