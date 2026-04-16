from Conectar_Banco import conectar_banco as minha_conexao
from Perguntas import Perguntas
from usuario import Usuario
import mysql.connector
import random

lista_perguntas = []

def iniciar_jogo():
    score_atual = 0
    conexao_ativa = minha_conexao()
    cursor = conexao_ativa.cursor(dictionary=True)

    cursor.execute("SELECT * FROM PERGUNTAS")
    perguntas_do_banco = cursor.fetchall()

    for i in perguntas_do_banco:
        perguntas_objeto = Perguntas(i)
        lista_perguntas.append(perguntas_objeto)

    random.shuffle(lista_perguntas)

    Usuario.login()
    

    for pergunta in lista_perguntas:
        pergunta.exibir_pergunta()
        resposta = input("Selecione a alternativa correta: ")
        if resposta == 'Dica':
            print(pergunta.dica)
            resposta = input("Selecione a alternativa correta: ")
        
        if resposta.upper() == pergunta.correta:
            print(f"Você acertou e conseguiu {pergunta.pontos} ")
            score_atual += pergunta.pontos
        
        else:
            print("Você errou!")
        print(f"Sua pontuação atual: {score_atual} pontos!")   

    cursor.close()
    conexao_ativa.close()     


iniciar_jogo()