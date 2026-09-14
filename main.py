import subprocess
import sys


def executar_script(nome_script):

    print("\n")
    print("=" * 50)
    print(f"EXECUTANDO: {nome_script}")
    print("=" * 50)

    resultado = subprocess.run(
        [sys.executable, nome_script]
    )

    if resultado.returncode != 0:

        print(f"\nErro ao executar {nome_script}")
        return False

    print(f"\n{nome_script} finalizado com sucesso.")

    return True


def main():

    print("=" * 50)
    print("       CHARGEGRID INTELLIGENCE")
    print("       SISTEMA DE AUTOMAÇÃO")
    print("=" * 50)

    print("\nIniciando ciclo de gerenciamento energético...")

    # 1. Analisa os estados e cria comandos
    sucesso = executar_script(
        "gerenciamento_demanda.py"
    )

    if not sucesso:
        print("\nO processo foi interrompido.")
        return

    # 2. Executa os comandos criados
    sucesso = executar_script(
        "executor_comandos.py"
    )

    if not sucesso:
        print("\nO processo foi interrompido.")
        return

    print("\n")
    print("=" * 50)
    print("       CICLO CONCLUÍDO")
    print("=" * 50)

    print("\nEstados analisados")
    print("Comandos processados")
    print("Carregadores atualizados")
    print("Automação finalizada")


if __name__ == "__main__":
    main()