from Jogo import iniciar_jogo
from professor import Professor

print("INICIAR")
print("1 - Sou aluno")
print("2 - Sou professor")
opcao = input("Opção: ").strip()

if opcao == "1":
    iniciar_jogo()

elif opcao == "2":

    print("\n1 - Login")
    print("2 - Cadastrar")
    escolha = input("Opção: ").strip()

    if escolha == "1":
        prof = Professor.login()

    elif escolha == "2":
        prof = Professor.cadastrar()

    else:
        print("Opção inválida.")
        prof = None

    if prof:
        prof.menu()

else:
    print("Opção inválida.")