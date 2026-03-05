import pandas as pd
from pathlib import Path

INPUT_DIR = Path("data/raw/precatorios")
OUTPUT_FILE = Path("data/processed/precatorios_tjpi.csv")


def carregar_csvs():

    arquivos = list(INPUT_DIR.glob("*.csv"))

    dfs = []

    for arquivo in arquivos:

        print(f"Lendo {arquivo.name}")

        df = pd.read_csv(arquivo)

        # garantir apenas 9 colunas
        df = df.iloc[:, :9]

        df.columns = [
            "posicao",
            "ente_devedor",
            "ano",
            "natureza",
            "data_entrada_oficio",
            "numero_pje",
            "tipo",
            "valor",
            "observacoes"
        ]

        dfs.append(df)

    return dfs


def limpar_dados(df):

    # posição
    df["posicao"] = (
        df["posicao"]
        .astype(str)
        .str.replace("º", "", regex=False)
    )
    df["posicao"] = pd.to_numeric(df["posicao"], errors="coerce")

    # ano
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")

    # limpar valor monetário
    df["valor"] = (
        df["valor"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    # remover linhas totalmente duplicadas
    df = df.drop_duplicates()

    # remover duplicados de precatórios (mesmo processo + tipo)
    antes = len(df)

    df = df.drop_duplicates(subset=["numero_pje", "tipo"])

    depois = len(df)

    print(f"Duplicados removidos: {antes - depois}")

    return df


def main():

    print("Iniciando transformação...\n")

    dfs = carregar_csvs()

    df_final = pd.concat(dfs, ignore_index=True)

    print("Registros antes da limpeza:", len(df_final))

    df_final = limpar_dados(df_final)

    print("Registros após limpeza:", len(df_final))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df_final.to_csv(OUTPUT_FILE, index=False)

    print("\nTransformação concluída")
    print("Dataset salvo em:", OUTPUT_FILE)
    print("Total de registros finais:", len(df_final))


if __name__ == "__main__":
    main()