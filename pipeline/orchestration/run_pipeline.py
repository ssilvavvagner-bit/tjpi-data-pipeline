import subprocess
import sys


def executar_etapa(nome, comando):

    print(f"\n🚀 Iniciando etapa: {nome}")

    resultado = subprocess.run(comando, shell=True)

    if resultado.returncode != 0:
        print(f"\n❌ Erro na etapa: {nome}")
        sys.exit(1)

    print(f"✅ Etapa concluída: {nome}")


def main():

    print("\n===============================")
    print("PIPELINE TJPI PRECATORIOS")
    print("===============================\n")

    executar_etapa(
        "INGESTION (SCRAPER)",
        "python pipeline/ingestion/scraper_tjpi_precatorios.py"
    )

    executar_etapa(
        "PROCESSING (TRANSFORM)",
        "python pipeline/processing/transform_precatorios.py"
    )

    executar_etapa(
        "LOAD (POSTGRES)",
        "python pipeline/loaders/load_precatorios_postgres.py"
    )

    print("\n===============================")
    print("PIPELINE FINALIZADO COM SUCESSO")
    print("===============================")


if __name__ == "__main__":
    main()