class Perguntas:
    def __init__(self,data):
        self.enunciado = data['Enunciado']
        self.id = data['ID']
        self.opcoes= self.opcoes = {
            'A': data['Opcao_A'], # PRECISA ser dois pontos (:)
            'B': data['Opcao_B'],
            'C': data['Opcao_C'],
            'D': data['Opcao_D']
        }
        self.correta = data['Correta'].upper()
        self.dica = data['Dica']
        self.pontos = data['Pontuacao']
    
    def exibir_pergunta (self):
        print(f"\n{'='*5} Valendo {self.pontos} pontos {'='*5}")
        print(f"Pergunta: {self.enunciado}")
        for letra, texto in self.opcoes.items():
            print(f"{letra}) {texto}")


