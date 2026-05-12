<<<<<<< HEAD
from Conectar_Banco import conectar_banco as minha_conexao
from Perguntas import Perguntas
from aluno import aluno
import mysql.connector
import random

def iniciar_jogo():
    conexao_ativa = minha_conexao()
    cursor = conexao_ativa.cursor(dictionary=True)

    
    usuario_logado = aluno.menu()
    if not usuario_logado:
        return

    dificuldade = input(f"\n{'='*10} Selecione sua dificuldade {'='*10}\n 0 - Sair \n 1 - Fácil \n 2 - Médio \n 3 - Difícil \n 4 - Aleatório \n Opção: ")
    
    if dificuldade == "0":
        print("Saindo...")
        return

    if dificuldade == "1":
        cursor.execute("SELECT * FROM PERGUNTAS WHERE DIFICULDADE = 'Fácil'")
    elif dificuldade == "2":
        cursor.execute("SELECT * FROM PERGUNTAS WHERE DIFICULDADE = 'Médio'")
    elif dificuldade == "3":
        cursor.execute("SELECT * FROM PERGUNTAS WHERE DIFICULDADE = 'Difícil'")
    elif dificuldade == "4":
        cursor.execute("SELECT * FROM PERGUNTAS") 
    else:
        print("Opção inválida!")
        return


    perguntas_do_banco = cursor.fetchall()
    lista_perguntas = [Perguntas(p) for p in perguntas_do_banco]
    random.shuffle(lista_perguntas)


    for pergunta in lista_perguntas:
        pergunta.exibir_pergunta()
        resposta = input("Selecione a alternativa (ou 'Dica'): ").strip()
        
        if resposta.lower() == 'dica':
            print(f"Dica: {pergunta.dica}")
            resposta = input("Sua resposta: ").strip()
        
        if resposta.upper() == pergunta.correta.upper():
            print(f"Você ganhou {pergunta.pontos} pontos.")
            usuario_logado.pontos += pergunta.pontos

            codigo = 'UPDATE USUARIO SET Pontuacao = %s WHERE ID = %s'
            cursor.execute(codigo, (usuario_logado.pontos, usuario_logado.id))
            conexao_ativa.commit()
        else:
            print(f"A resposta era {pergunta.correta}")
        
        print(f"Score atual: {usuario_logado.pontos}")

    cursor.close()
    conexao_ativa.close()     

if __name__ == "__main__":
=======
from Conectar_Banco import conectar_banco as minha_conexao
from Perguntas import Perguntas
from aluno import aluno
import mysql.connector
import random

def iniciar_jogo():
    conexao_ativa = minha_conexao()
    cursor = conexao_ativa.cursor(dictionary=True)

    
    usuario_logado = aluno.menu()
    if not usuario_logado:
        return

    dificuldade = input(f"\n{'='*10} Selecione sua dificuldade {'='*10}\n 0 - Sair \n 1 - Fácil \n 2 - Médio \n 3 - Difícil \n 4 - Aleatório \n Opção: ")
    
    if dificuldade == "0":
        print("Saindo...")
        return

    if dificuldade == "1":
        cursor.execute("SELECT * FROM PERGUNTAS WHERE DIFICULDADE = 'Fácil'")
    elif dificuldade == "2":
        cursor.execute("SELECT * FROM PERGUNTAS WHERE DIFICULDADE = 'Médio'")
    elif dificuldade == "3":
        cursor.execute("SELECT * FROM PERGUNTAS WHERE DIFICULDADE = 'Difícil'")
    elif dificuldade == "4":
        cursor.execute("SELECT * FROM PERGUNTAS") 
    else:
        print("Opção inválida!")
        return


    perguntas_do_banco = cursor.fetchall()
    lista_perguntas = [Perguntas(p) for p in perguntas_do_banco]
    random.shuffle(lista_perguntas)


    for pergunta in lista_perguntas:
        pergunta.exibir_pergunta()
        resposta = input("Selecione a alternativa (ou 'Dica'): ").strip()
        
        if resposta.lower() == 'dica':
            print(f"Dica: {pergunta.dica}")
            resposta = input("Sua resposta: ").strip()
        
        if resposta.upper() == pergunta.correta.upper():
            print(f"Você ganhou {pergunta.pontos} pontos.")
            usuario_logado.pontos += pergunta.pontos

            codigo = 'UPDATE USUARIO SET Pontuacao = %s WHERE ID = %s'
            cursor.execute(codigo, (usuario_logado.pontos, usuario_logado.id))
            conexao_ativa.commit()
        else:
            print(f"A resposta era {pergunta.correta}")
        
        print(f"Score atual: {usuario_logado.pontos}")

    cursor.close()
    conexao_ativa.close()     

if __name__ == "__main__":
>>>>>>> 66ba91564e7fb655c9df26d46278a64f1a976b55
    iniciar_jogo()