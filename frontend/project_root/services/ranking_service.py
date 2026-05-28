# =========================================================
# ORDENAR RANKING DE ALUNOS
# =========================================================

def ordenar_ranking_alunos(ranking_alunos):

    return sorted(
        ranking_alunos,
        key=lambda aluno: aluno["pontos"],
        reverse=True
    )


# =========================================================
# ORDENAR RANKING DE TURMAS
# =========================================================

def ordenar_ranking_turmas(ranking_turmas):

    return sorted(
        ranking_turmas,
        key=lambda turma: turma["pontos"],
        reverse=True
    )


# =========================================================
# CALCULAR MÉDIA
# =========================================================

def calcular_media(acertos, total):

    if total == 0:
        return 0

    return round(acertos / total, 2)


# =========================================================
# ADICIONAR PONTOS
# =========================================================

def adicionar_pontos(aluno, pontos):

    aluno["pontos"] += pontos


# =========================================================
# FILTRAR TURMA
# =========================================================

def filtrar_por_turma(ranking_alunos, turma):

    return [
        aluno
        for aluno in ranking_alunos
        if aluno["turma"] == turma
    ]