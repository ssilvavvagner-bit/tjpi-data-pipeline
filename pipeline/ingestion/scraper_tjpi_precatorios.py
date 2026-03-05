import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_LISTA = "https://www.tjpi.jus.br/sapre/sapre/ordempagamento/listar/"
URL_ENTES = "https://www.tjpi.jus.br/sapre/sapre/publico/entes-regime-especial/"

OUTPUT_DIR = "data/raw/precatorios"

os.makedirs(OUTPUT_DIR, exist_ok=True)

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0"
}


def descobrir_entes():

    print("Descobrindo entes...")

    r = session.get(URL_ENTES, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    tabela = soup.find("table")

    entes = []

    for linha in tabela.find_all("tr")[1:]:

        colunas = linha.find_all("td")

        if len(colunas) < 4:
            continue

        nome = colunas[0].text.strip()

        link = colunas[3].find("a")

        if not link:
            continue

        href = link.get("href")

        match = re.search(r"enteDevedor=(\d+)", href)

        if not match:
            continue

        ente_id = match.group(1)

        nome_arquivo = nome.lower()
        nome_arquivo = re.sub(r"[^\w\s]", "", nome_arquivo)
        nome_arquivo = nome_arquivo.replace(" ", "_")

        entes.append((ente_id, nome, nome_arquivo))

    print("Total de entes encontrados:", len(entes))

    return entes


def baixar_ente(ente):

    ente_id, nome, nome_arquivo = ente

    caminho = f"{OUTPUT_DIR}/{nome_arquivo}.csv"

    # INCREMENTAL: se já existe, pula
    if os.path.exists(caminho):

        print(f"⏭️  Pulando {nome} (já existe)")

        return 0

    print(f"\nBaixando {nome}")

    page = 1
    todos = []

    while True:

        params = {
            "enteDevedor": ente_id,
            "page": page,
            "qtd": 100
        }

        try:

            r = session.get(BASE_LISTA, params=params, headers=headers, timeout=20)

        except:

            print(f"erro conexão {nome} página {page}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")

        tabela = soup.find("table")

        if not tabela:
            break

        linhas = tabela.find_all("tr")[1:]

        if len(linhas) == 0:
            break

        for linha in linhas:

            cols = [c.text.strip() for c in linha.find_all("td")]

            todos.append(cols)

        print(f"{nome} | página {page} | registros {len(linhas)}")

        if len(linhas) < 100:
            break

        page += 1

    if len(todos) == 0:
        return 0

    df = pd.DataFrame(todos)

    df.to_csv(caminho, index=False)

    print(f"✔ {nome} concluído | {len(df)} registros")

    return len(df)


def main():

    entes = descobrir_entes()

    total_registros = 0

    print("\nIniciando scraping paralelo...\n")

    with ThreadPoolExecutor(max_workers=6) as executor:

        futures = [executor.submit(baixar_ente, ente) for ente in entes]

        for future in as_completed(futures):

            total_registros += future.result()

    print("\n===============================")
    print("SCRAPER FINALIZADO")
    print("Entes processados:", len(entes))
    print("Registros coletados:", total_registros)
    print("===============================")


if __name__ == "__main__":
    main()