import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def buscar_comandos_pendentes():
    resposta = (
        supabase
        .table("comandos_de_automacao")
        .select("*")
        .eq("executado", False)
        .order("id")
        .execute()
    )

    return resposta.data


def atualizar_carregador(carregador_id, nova_potencia):
    resposta = (
        supabase
        .table("carregadores")
        .update({
            "potencia_kw": nova_potencia
        })
        .eq("id", carregador_id)
        .execute()
    )

    return resposta.data


def executar_comando(comando):

    comando_id = comando["id"]
    carregador_id = comando["carregador_id"]
    nova_potencia = float(comando["potencia_nova_kw"])

    print("\n==============================")
    print(f"Executando comando: {comando_id}")
    print(f"Tipo: {comando['tipo_comando']}")
    print(f"Carregador: {carregador_id}")
    print(
        f"Potência: "
        f"{comando['potencia_anterior_kw']} → "
        f"{nova_potencia} kW"
    )

    # Atualiza o carregador
    atualizar_carregador(
        carregador_id,
        nova_potencia
    )

    # Registra a execução
    agora = datetime.now(timezone.utc).isoformat()

    supabase \
        .table("comandos_de_automacao") \
        .update({
            "executado": True,
            "executado_em": agora
        }) \
        .eq("id", comando_id) \
        .execute()

    print("✅ Comando executado com sucesso!")


def main():

    print("================================")
    print("     CHARGEGRID INTELLIGENCE")
    print("     EXECUTOR DE COMANDOS")
    print("================================")

    comandos = buscar_comandos_pendentes()

    print(f"\nComandos pendentes: {len(comandos)}")

    if not comandos:
        print("Nenhum comando pendente.")
        return

    for comando in comandos:
        executar_comando(comando)


if __name__ == "__main__":
    main()