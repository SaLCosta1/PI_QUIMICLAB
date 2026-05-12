from Conectar_Banco import conectar_banco

conexao = conectar_banco()
cursor = conexao.cursor(dictionary=True, buffered=True)

class Professor:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nome = data['nome']
        self.email = data['email']

    def cadastrar():
        print("\n--- CADASTRAR PROFESSOR ---")

        nome = input("Nome completo: ").strip()
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()

        cursor.execute(
            "SELECT * FROM usuario WHERE email = %s",
            (email,)
        )
        existente = cursor.fetchone()

        if existente:
            print("Email já cadastrado.")
            return None

        cursor.execute(
            "INSERT INTO usuario (nome, email, senha_hash, tipo) VALUES (%s, %s, %s, 'professor')",
            (nome, email, senha)
        )
        conexao.commit()

        cursor.execute(
            "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s",
            (email, senha)
        )

        dados = cursor.fetchone()

        print(f"Professor {nome} cadastrado com sucesso!")
        return Professor(dados)
    def login():
        print("\n--- LOGIN PROFESSOR ---")
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()

        cursor.execute(
            "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s AND tipo = 'professor'",
            (email, senha)
        )
        dados = cursor.fetchone()

        if dados:
            print(f"Bem-vindo, professor {dados['nome']}!")
            return Professor(dados)
        else:
            print("Credenciais invalidas.")
            return None
    
    def ver_perguntas(self):

        cursor.execute("""
            SELECT
            p.id_pergunta,
            p.enunciado,
            n.nome AS nivel
        FROM pergunta p
        JOIN nivel n ON n.id_nivel = p.id_nivel
        ORDER BY p.id_pergunta
        """)

        print("\n - Perguntas Cadastradas - ")

        perguntas = cursor.fetchall()


        for p in perguntas:
            print(f"\nNúmero: {p['id_pergunta']}")
            print(f"Dificuldade: {p['nivel']}")
            print(f"Enunciado: {p['enunciado']}")

        cursor.execute(
            "SELECT * FROM alternativa WHERE id_pergunta = %s",
            (p['id_pergunta'],)
        )

        alternativas = cursor.fetchall()

        letras = ['A', 'B', 'C', 'D']

        for i in range(len(alternativas)):

            correta = ""

            if alternativas[i]['correta'] == 1:
                correta = " (CORRETA)"

            print(
                f"{letras[i]}) "
                f"{alternativas[i]['texto']}"
                f"{correta}"
            )

        cursor.execute(
            "SELECT * FROM dica WHERE id_pergunta = %s",
            (p['id_pergunta'],)
        )

        dica = cursor.fetchone()

        if dica:
            print(f"Dica: {dica['conteudo']}")

    def editar_pergunta(self):

            self.ver_perguntas()

            id_pergunta = input(
                "\nDigite o número da pergunta que deseja editar: "
            ).strip()

            cursor.execute(
                "SELECT * FROM pergunta WHERE id_pergunta = %s",
                (id_pergunta,)
            )

            pergunta = cursor.fetchone()

            if not pergunta:
                print("Pergunta nao encontrada.")
                return

            print("\n1 - Editar enunciado")
            print("2 - Editar alternativas")
            print("3 - Editar dica")

            opcao = input("Opcao: ").strip()

            if opcao == "1":

                novo = input("Novo enunciado: ").strip()

                cursor.execute(
                    """
                    UPDATE pergunta
                    SET enunciado = %s
                    WHERE id_pergunta = %s
                    """,
                    (novo, id_pergunta)
                )

                conexao.commit()

                print("Enunciado atualizado!")

            elif opcao == "2":

                cursor.execute(
                    "SELECT * FROM alternativa WHERE id_pergunta = %s",
                    (id_pergunta,)
                )

                alternativas = cursor.fetchall()

                letras = ['A', 'B', 'C', 'D']

                print("\nAlternativas atuais:")

                for i in range(len(alternativas)):
                    print(f"{letras[i]}) {alternativas[i]['texto']}")

                letra_editar = input(
                    "Qual alternativa deseja editar? "
                ).strip().upper()

                if letra_editar not in letras:
                    print("Alternativa invalida.")
                    return

                indice = letras.index(letra_editar)

                novo_texto = input(
                    "Novo texto da alternativa: "
                ).strip()

                cursor.execute(
                    """
                    UPDATE alternativa
                    SET texto = %s
                    WHERE id_alternativa = %s
                    """,
                    (
                        novo_texto,
                        alternativas[indice]['id_alternativa']
                    )
                )

                nova_correta = input(
                    "Essa alternativa sera a correta? (S/N): "
                ).strip().upper()

                if nova_correta == "S":

                    cursor.execute(
                        """
                        UPDATE alternativa
                        SET correta = 0
                        WHERE id_pergunta = %s
                        """,
                        (id_pergunta,)
                    )

                    cursor.execute(
                        """
                        UPDATE alternativa
                        SET correta = 1
                        WHERE id_alternativa = %s
                        """,
                        (alternativas[indice]['id_alternativa'],)
                    )

                conexao.commit()

                print("Alternativa atualizada!")

            elif opcao == "3":

                cursor.execute(
                    "SELECT * FROM dica WHERE id_pergunta = %s",
                    (id_pergunta,)
                )

                dica = cursor.fetchone()

                if not dica:
                    print("Pergunta sem dica.")
                    return

                nova_dica = input("Nova dica: ").strip()

                cursor.execute(
                    """
                    UPDATE dica
                    SET conteudo = %s
                    WHERE id_dica = %s
                    """,
                    (nova_dica, dica['id_dica'])
                )

                conexao.commit()

                print("Dica atualizada!")

            else:
                print("Opcao invalida.")

    def cadastrar_pergunta(self):
        print("\n--- CADASTRAR PERGUNTA ---")
        print("1 - Facil")
        print("2 - Medio")
        print("3 - Dificil")

        opcao = input("Dificuldade: ").strip()

        if opcao == "1":
            id_nivel = 1
        elif opcao == "2":
            id_nivel = 2
        elif opcao == "3":
            id_nivel = 3
        else:
            print("Opcao invalida.")
            return

        enunciado = input("Enunciado: ").strip()

        cursor2 = conexao.cursor()

        cursor2.execute(
            "INSERT INTO pergunta (id_nivel, id_criador, enunciado) VALUES (%s, %s, %s)",
            (id_nivel, self.id_usuario, enunciado)
        )

        conexao.commit()
        id_pergunta = cursor2.lastrowid

        letras = ['A', 'B', 'C', 'D']
        alternativas_texto = []

        print("\nDigite as alternativas:")

        for letra in letras:
            texto = input(f"Alternativa {letra}: ").strip()

            if not texto:
                print("Todas as alternativas devem ser preenchidas.")
                return

            alternativas_texto.append(texto)

        correta = input(
            "\nQual letra e a correta? (A/B/C/D): "
        ).strip().upper()

        if correta not in letras:
            print("Alternativa correta invalida.")
            return

        for i in range(len(alternativas_texto)):

            eh_correta = 1 if letras[i] == correta else 0

            cursor2.execute(
                """
                INSERT INTO alternativa
                (id_pergunta, texto, correta)
                VALUES (%s, %s, %s)
                """,
                (
                    id_pergunta,
                    alternativas_texto[i],
                    eh_correta
                )
            )

        print("\n--- DICA ---")
        conteudo = input("Digite a dica da pergunta: ").strip()

        penalizacao = int(
            input("Penalizacao em pontos (0 para nenhuma): ").strip()
        )

        cursor2.execute(
            """
            INSERT INTO dica
            (id_pergunta, tipo, conteudo, penalizacao_pontos)
            VALUES (%s, %s, %s, %s)
            """,
            (
                id_pergunta,
                'texto',
                conteudo,
                penalizacao
            )
        )

        conexao.commit()
        cursor2.close()

        print("Pergunta cadastrada com sucesso!")

    def ver_desempenho(self):
        cursor.execute("SELECT * FROM vw_desempenho ORDER BY turma, nome")
        dados = cursor.fetchall()

        if not dados:
            print("Nenhum dado ainda.")
            return

        print(f"\n{'Nome':<25} {'Turma':<10} {'Nivel':<12} {'Acertos':<8} {'Taxa%'}")
        print(f"{'='*60}")
        for i in range(len(dados)):
            d = dados[i]
            print(f"{d['nome']:<25} {str(d['turma']):<10} {d['nivel']:<12} {str(d['acertos']):<8} {d['taxa_acerto_pct']}%")

    def ver_mais_erradas(self):
        cursor.execute("SELECT * FROM vw_questoes_mais_erradas LIMIT 10")
        dados = cursor.fetchall()

        if not dados:
            print("Nenhum dado ainda.")
            return

        print("\nTop questoes mais erradas:")
        print(f"{'='*60}")
        for i in range(len(dados)):
            d = dados[i]
            print(f"[{d['nivel']}] {d['enunciado'][:55]}... | {d['taxa_erro_pct']}% de erro")

    def menu(self):
        while True:

            print("\nMenu Professor")
            print("1 - Cadastrar pergunta")
            print("2 - Ver perguntas")
            print("3 - Editar pergunta")
            print("4 - Ver desempenho da turma")
            print("5 - Ver questoes mais erradas")
            print("0 - Sair")

            opcao = input("Opcao: ").strip()

            if opcao == "1":
                self.cadastrar_pergunta()

            elif opcao == "2":
                self.ver_perguntas()

            elif opcao == "3":
                self.editar_pergunta()

            elif opcao == "4":
                self.ver_desempenho()

            elif opcao == "5":
                self.ver_mais_erradas()

            elif opcao == "0":
                break

            else:
                print("Opcao invalida.")
