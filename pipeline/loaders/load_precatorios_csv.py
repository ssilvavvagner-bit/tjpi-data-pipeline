import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/processed/precatorios_tjpi.csv")


def main():

    print("Iniciando etapa LOAD...\n")

    df = pd.read_csv(INPUT_FILE)

    print("Dataset carregado com sucesso\n")

    print("Total de registros:", len(df))
    print("Total de entes:", df["ente_devedor"].nunique())

    print("\nResumo por ente:")
    print(df["ente_devedor"].value_counts().head(10))

    print("\nValor total de precatórios:")

    total_valor = df["valor"].sum()

    print(f"R$ {total_valor:,.2f}")


if __name__ == "__main__":
    main()