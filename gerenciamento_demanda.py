import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def buscar_estados():

    resposta = supabase.table("estado_energetico").select("*").order("id").execute()

    return resposta.data


def buscar_carregadores(estacao_id):

    resposta = (
        supabase.table("carregadores")
        .select("*")
        .eq("id_estacao", estacao_id)
        .execute()
    )

    print("\nCarregadores encontrados:")

    for carregador in resposta.data:
        print(carregador)

    return resposta.data


def existe_comando_pendente(carregador_id):

    resposta = (
        supabase.table("comandos_de_automacao")
        .select("id")
        .eq("carregador_id", carregador_id)
        .eq("executado", False)
        .limit(1)
        .execute()
    )

    return len(resposta.data) > 0


def criar_comando(
    tipo_comando, potencia_anterior, carregador_id, potencia_nova, motivo
):

    comando = {
        "tipo_comando": tipo_comando,
        "potencia_anterior_kw": potencia_anterior,
        "carregador_id": carregador_id,
        "potencia_nova_kw": potencia_nova,
        "motivo": motivo,
        "executado": False,
    }

    resposta = supabase.table("comandos_de_automacao").insert(comando).execute()

    print("\nComando criado no Supabase:")
    print(resposta.data)

    return resposta.data


def analisar_estado(estado):

    solar = float(estado["energia_solar_kW"])
    demanda = float(estado["demanda_kw"])
    disponibilidade = float(estado["potencia_disponivel_kw"])

    estacao_id = estado["estacao_id"]

    print("\n==============================")
    print(f"Estado energético ID: {estado['id']}")
    print(f"Estação: {estacao_id}")
    print(f"Energia solar: {solar} kW")
    print(f"Energia da rede: {estado['energia_rede_kw']} kW")
    print(f"Demanda: {demanda} kW")
    print(f"Potência disponível: {disponibilidade} kW")
    print(f"Bateria: {estado['bateria_percentual']}%")
    print(f"Status: {estado['status_gerenciamento']}")

    carregadores = buscar_carregadores(estacao_id)

    # ==========================
    # DEMANDA ELEVADA
    # ==========================

    if demanda > disponibilidade:

        carregador = next(
            (c for c in carregadores if c["status"].lower() == "ocupado"), None
        )

        if carregador:

            print("\nDECISÃO: REDUZIR")
            print(f"Carregador escolhido: {carregador['id']}")

            if existe_comando_pendente(carregador["id"]):

                print("Já existe um comando pendente para este carregador.")
                print("Nenhum novo comando será criado.")

                return

            potencia_atual = float(carregador["potencia_kw"])
            nova_potencia = max(potencia_atual - 50, 50)

            if nova_potencia < potencia_atual:

                print(f"Potência: {potencia_atual} → {nova_potencia} kW")

                criar_comando(
                    "REDUZIR",
                    potencia_atual,
                    carregador["id"],
                    nova_potencia,
                    "Demanda elevada",
                )

            else:

                print("\n⚪ CARREGADOR NO LIMITE MÍNIMO")
                print(f"Potência atual: {potencia_atual} kW")
                print("Nenhuma redução será realizada.")

    # ==========================
    # ENERGIA SOLAR DISPONÍVEL
    # ==========================

    elif estado["status_gerenciamento"] == "Energia solar disponível":

        carregador = next(
            (c for c in carregadores if c["status"].lower() == "livre"), None
        )

        if carregador:

            print("\nDECISÃO: AUMENTAR")
            print(f"Carregador escolhido: {carregador['id']}")

            if existe_comando_pendente(carregador["id"]):

                print("Já existe um comando pendente para este carregador.")
                print("Nenhum novo comando será criado.")

                return

            potencia_atual = float(carregador["potencia_kw"])
            nova_potencia = min(potencia_atual + 50, 200)

            if nova_potencia > potencia_atual:

                print(f"Potência: {potencia_atual} → {nova_potencia} kW")

                criar_comando(
                    "AUMENTAR",
                    potencia_atual,
                    carregador["id"],
                    nova_potencia,
                    "Energia solar disponível",
                )

            else:

                print("\nCARREGADOR NO LIMITE MÁXIMO")
                print(f"Potência atual: {potencia_atual} kW")
                print("Nenhum aumento será realizado.")

    # ==========================
    # NORMAL
    # ==========================

    else:

        print("\nDECISÃO: MANTER")
        print("Nenhum comando será criado.")


def main():

    print("================================")
    print("     CHARGEGRID INTELLIGENCE")
    print("     AUTOMAÇÃO ENERGÉTICA")
    print("================================")

    estados = buscar_estados()

    print(f"\nEstados encontrados: {len(estados)}")

    for estado in estados:
        analisar_estado(estado)


if __name__ == "__main__":
    main()
