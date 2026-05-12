import random
import time
from Conectar_Banco import conectar_banco
from Perguntas import Pergunta
from aluno import Usuario

conexao = conectar_banco()
cursor = conexao.cursor(dictionary=True, buffered=True)

def carregar_perguntas(dificuldade):
    if dificuldade == "1":
        cursor.execute("SELECT * FROM pergunta WHERE id_nivel = 1 AND ativa = 1")
    elif dificuldade == "2":
        cursor.execute("SELECT * FROM pergunta WHERE id_nivel = 2 AND ativa = 1")
    elif dificuldade == "3":
        cursor.execute("SELECT * FROM pergunta WHERE id_nivel = 3 AND ativa = 1")
    elif dificuldade == "4":
        cursor.execute("SELECT * FROM pergunta WHERE ativa = 1")
    elif dificuldade == "5":
        cursor.execute("SELECT * FROM pergunta WHERE ativa = 1 ORDER BY id_nivel ASC")

    linhas = cursor.fetchall()

    if dificuldade == "5":
        linhas = linhas[:30]

    lista = []
    for i in range(len(linhas)):
        cursor.execute("SELECT * FROM alternativa WHERE id_pergunta = %s", (linhas[i]['id_pergunta'],))
        alternativas = cursor.fetchall()

        cursor.execute("SELECT * FROM dica WHERE id_pergunta = %s", (linhas[i]['id_pergunta'],))
        dicas = cursor.fetchall()

        lista.append(Pergunta(linhas[i], alternativas, dicas))

    return lista

def registrar_resposta(id_sessao, pergunta, alternativa_escolhida, correta, tempo_seg):
    cursor.execute(
        "INSERT INTO resposta (id_sessao, id_pergunta, id_alternativa_escolhida, correta, tempo_resposta_seg) VALUES (%s, %s, %s, %s, %s)",
        (id_sessao, pergunta.id_pergunta, alternativa_escolhida['id_alternativa'], correta, tempo_seg)
    )
    conexao.commit()

def atualizar_ranking(id_usuario, id_nivel, pontuacao):
    cursor.execute("SELECT * FROM ranking WHERE id_usuario = %s AND id_nivel = %s", (id_usuario, id_nivel))
    existente = cursor.fetchone()

    if existente:
        nova_melhor = max(existente['melhor_pontuacao'], pontuacao)
        cursor.execute(
            "UPDATE ranking SET melhor_pontuacao = %s, total_tentativas = total_tentativas + 1 WHERE id_usuario = %s AND id_nivel = %s",
            (nova_melhor, id_usuario, id_nivel)
        )
    else:
        cursor.execute(
            "INSERT INTO ranking (id_usuario, id_nivel, melhor_pontuacao, total_tentativas) VALUES (%s, %s, %s, 1)",
            (id_usuario, id_nivel, pontuacao)
        )
    conexao.commit()

def exibir_ranking(id_nivel):
    cursor.execute(
        "SELECT u.nome, r.melhor_pontuacao FROM ranking r JOIN usuario u ON u.id_usuario = r.id_usuario WHERE r.id_nivel = %s ORDER BY r.melhor_pontuacao DESC LIMIT 10",
        (id_nivel,)
    )
    dados = cursor.fetchall()

    print("\nRANKING")
    for i in range(len(dados)):
        print(f"{i+1}. {dados[i]['nome']:<25} {dados[i]['melhor_pontuacao']} pts")

def iniciar_jogo():
    usuario_logado = Usuario.menu()
    if not usuario_logado:
        return

    print("\nSelecione a dificuldade")
    print("1 - Facil")
    print("2 - Medio")
    print("3 - Dificil")
    print("4 - Aleatorio")
    print("5 - Jogo do Milhão")
    print("0 - Sair")

    dificuldade = input("Opcao: ").strip()

    if dificuldade == "0":
        return

    if dificuldade not in ["1", "2", "3", "4", "5"]:
        print("Opcao inválida.")
        return

    lista_perguntas = carregar_perguntas(dificuldade)

    if dificuldade != "5":
        random.shuffle(lista_perguntas)

    id_nivel = int(dificuldade) if dificuldade in ["1", "2", "3"] else 1

    cursor.execute(
        "INSERT INTO sessao_jogo (id_usuario, id_nivel) VALUES (%s, %s)",
        (usuario_logado.id_usuario, id_nivel)
    )
    conexao.commit()
    id_sessao = cursor.lastrowid

    pontuacao = 0
    acertos = 0
    letras = ['A', 'B', 'C', 'D', 'E']

    for i in range(len(lista_perguntas)):
        pergunta = lista_perguntas[i]
        print(f"\nPergunta {i+1}/{len(lista_perguntas)}")
        pergunta.exibir_pergunta()

        penalizacao = 0
        resposta = input("\nResposta: ").strip().upper()

        if resposta == "DICA":
            dica = pergunta.dicas[0]
            print(f"Dica: {dica['conteudo']}")
            penalizacao = dica['penalizacao_pontos']
            cursor.execute(
                "INSERT INTO uso_dica (id_sessao, id_pergunta, id_dica) VALUES (%s, %s, %s)",
                (id_sessao, pergunta.id_pergunta, dica['id_dica'])
            )
            conexao.commit()
            inicio = time.time()
            resposta = input("Resposta: ").strip().upper()
            tempo_seg = int(time.time() - inicio)
        else:
            tempo_seg = 0

        alternativa_escolhida = pergunta.alternativa_por_letra(resposta)
        if not alternativa_escolhida:
            print("Letra invalida, pulando.")
            continue

        correta = alternativa_escolhida['correta'] == 1
        registrar_resposta(id_sessao, pergunta, alternativa_escolhida, correta, tempo_seg)

        if correta:
            pontos = max(0, 10 - penalizacao)
            pontuacao += pontos
            acertos += 1
            print(f"Correto! +{pontos} pontos")
        else:
            alt_certa = pergunta.alternativa_correta()
            idx_certa = pergunta.alternativas.index(alt_certa)
            print(f"Errado! A resposta certa era {letras[idx_certa]}) {alt_certa['texto']}")

        print(f"Score: {pontuacao}")

    cursor.execute(
        "UPDATE sessao_jogo SET pontuacao = %s, concluida = 1, finalizado_em = NOW() WHERE id_sessao = %s",
        (pontuacao, id_sessao)
    )
    conexao.commit()

    atualizar_ranking(usuario_logado.id_usuario, id_nivel, pontuacao)

    taxa = round(acertos * 100 / len(lista_perguntas), 1)
    print(f"\nFim! Acertos: {acertos}/{len(lista_perguntas)} ({taxa}%)")
    print(f"Pontuacao final: {pontuacao}")

    exibir_ranking(id_nivel)

if __name__ == "__main__":
    iniciar_jogo()
