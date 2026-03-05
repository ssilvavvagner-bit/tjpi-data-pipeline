import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = "data/processed/precatorios_tjpi.csv"


def conectar():

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    return conn


def carregar_csv():

    df = pd.read_csv(CSV_PATH)

    print("\nDataset carregado:", len(df), "registros")

    return df


def inserir_dados(conn, df):

    cursor = conn.cursor()

    query = """
    INSERT INTO precatorios (
        posicao,
        ente_devedor,
        ano,
        natureza,
        data_entrada_oficio,
        numero_pje,
        tipo,
        valor,
        observacoes
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)

    ON CONFLICT (numero_pje, tipo)
    DO UPDATE SET
        posicao = EXCLUDED.posicao,
        ente_devedor = EXCLUDED.ente_devedor,
        ano = EXCLUDED.ano,
        natureza = EXCLUDED.natureza,
        data_entrada_oficio = EXCLUDED.data_entrada_oficio,
        tipo = EXCLUDED.tipo,
        valor = EXCLUDED.valor,
        observacoes = EXCLUDED.observacoes
    """

    total = len(df)

    for i, row in df.iterrows():

        cursor.execute(query, (
            row["posicao"],
            row["ente_devedor"],
            row["ano"],
            row["natureza"],
            row["data_entrada_oficio"],
            row["numero_pje"],
            row["tipo"],
            row["valor"],
            row["observacoes"]
        ))

        if i % 500 == 0:
            print(f"Inseridos {i} registros...")

    conn.commit()

    print("\nInserção finalizada:", total, "registros")


def main():

    print("\nIniciando LOAD PostgreSQL...")

    df = carregar_csv()

    conn = conectar()

    inserir_dados(conn, df)

    conn.close()


if __name__ == "__main__":
    main()