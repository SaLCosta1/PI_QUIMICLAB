<<<<<<< HEAD
from Conectar_Banco import conectar_banco as minha_conexao
from Perguntas import Perguntas
from usuario import Usuario
import mysql.connector
import random

lista_perguntas = []

def iniciar_jogo():
    
    conexao_ativa = minha_conexao()
    cursor = conexao_ativa.cursor(dictionary=True)

    cursor.execute("SELECT * FROM PERGUNTAS")
    perguntas_do_banco = cursor.fetchall()

    for i in perguntas_do_banco:
        perguntas_objeto = Perguntas(i)
        lista_perguntas.append(perguntas_objeto)

    random.shuffle(lista_perguntas)

    usuario_logado = Usuario.login()
    score_atual = usuario_logado.pontos
    

    for pergunta in lista_perguntas:
        pergunta.exibir_pergunta()
        resposta = input("Selecione a alternativa correta: ")
        if resposta == 'Dica':
            print(pergunta.dica)
            resposta = input("Selecione a alternativa correta: ")
        
        if resposta.upper() == pergunta.correta:
            print(f"Você acertou e conseguiu {pergunta.pontos} ")
            usuario_logado.pontos += pergunta.pontos
            codigo = ('UPDATE USUARIO SET Pontuacao = %s WHERE ID = %s')
            cursor.execute(codigo, (usuario_logado.pontos, usuario_logado.id))
            conexao_ativa.commit()
        else:
            print("Você errou!")
        print(f"Sua pontuação atual: {usuario_logado.pontos} pontos!")   

    cursor.close()
    conexao_ativa.close()     


=======
from Conectar_Banco import conectar_banco as minha_conexao
from Perguntas import Perguntas
from usuario import Usuario
import mysql.connector
import random

lista_perguntas = []

def iniciar_jogo():
    
    conexao_ativa = minha_conexao()
    cursor = conexao_ativa.cursor(dictionary=True)

    cursor.execute("SELECT * FROM PERGUNTAS")
    perguntas_do_banco = cursor.fetchall()

    for i in perguntas_do_banco:
        perguntas_objeto = Perguntas(i)
        lista_perguntas.append(perguntas_objeto)

    random.shuffle(lista_perguntas)

    usuario_logado = Usuario.login()
    score_atual = usuario_logado.pontos
    

    for pergunta in lista_perguntas:
        pergunta.exibir_pergunta()
        resposta = input("Selecione a alternativa correta: ")
        if resposta == 'Dica':
            print(pergunta.dica)
            resposta = input("Selecione a alternativa correta: ")
        
        if resposta.upper() == pergunta.correta:
            print(f"Você acertou e conseguiu {pergunta.pontos} ")
            usuario_logado.pontos += pergunta.pontos
            codigo = ('UPDATE USUARIO SET Pontuacao = %s WHERE ID = %s')
            cursor.execute(codigo, (usuario_logado.pontos, usuario_logado.id))
            conexao_ativa.commit()
        else:
            print("Você errou!")
        print(f"Sua pontuação atual: {usuario_logado.pontos} pontos!")   

    cursor.close()
    conexao_ativa.close()     


>>>>>>> 66ba91564e7fb655c9df26d46278a64f1a976b55
iniciar_jogo()