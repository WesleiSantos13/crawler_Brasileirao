import requests
from bs4 import BeautifulSoup
import csv


# Nome correto das tabelas
nomes_tabelas = {
    0: "Participantes.csv",
    1: "Classificacao.csv",
    2: "Confrontos.csv",
    3: "Artilharia.csv",
    4: "Assistencia.csv",
    5: "Hat_tricks.csv"
}


# Lista de anos que serão coletados
anos = [2023, 2024, 2025]

# Mapeamento dos índices das tabelas para cada ano
# (porque a posição das tabelas muda na Wikipedia)
mapa_indices = {
    2025: [1, 3, 4, 6, 7, 8],
    2024: [0, 2, 3, 5, 6, 8],
    2023: [0, 2, 3, 5, 6, 8]
}

# Header para evitar bloqueio do request (simula navegador)
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Dicionário para controlar se o cabeçalho já foi escrito
cabecalho_escrito = {}

# Loop principal: percorre cada ano
for ANO in anos:

    # Monta a URL dinamicamente para cada ano
    url = f"https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{ANO}_-_Série_A"

    # Faz a requisição da página
    response = requests.get(url, headers=headers)

    # Converte o HTML em objeto manipulável
    soup = BeautifulSoup(response.text, "lxml")

    # Busca todas as tabelas da página
    tables = soup.find_all("table", class_="wikitable")

    # Pega os índices corretos para aquele ano
    indices = mapa_indices[ANO]

    # Percorre as tabelas desejadas
    for idx_padrao, i in enumerate(indices):

        # Evita erro caso o índice não exista
        if i >= len(tables):
            continue

        table = tables[i]

        # Nome do arquivo (mesmo arquivo para todos os anos)
        nome_arquivo = nomes_tabelas[idx_padrao]

        # Abre o arquivo em modo append (acrescenta dados)
        with open(nome_arquivo, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # =========================
            # TRATAMENTO IMPORTANTE: TABELA DE CONFRONTOS
            # =========================
            if idx_padrao == 2:
                rows = table.find_all("tr")

                # Primeira linha contém os times visitantes
                header = [th.get_text(strip=True) for th in rows[0].find_all("th")][1:]

                # Escreve cabeçalho apenas uma vez
                if not cabecalho_escrito.get(idx_padrao):
                    writer.writerow(["Mandante", "Placar", "Visitante", "Ano"])
                    cabecalho_escrito[idx_padrao] = True

                # Percorre as linhas (times mandantes)
                for r in range(1, len(rows)):
                    cells = rows[r].find_all(["td", "th"])

                    # Primeiro elemento da linha = time mandante
                    mandante = cells[0].get_text(strip=True)

                    # Percorre os confrontos (colunas)
                    for c in range(1, len(cells)):
                        placar = cells[c].get_text(strip=True).strip()

                        # Ignora células vazias ou com traço
                        if not placar or all(x in "-–— " for x in placar):
                            continue

                        # Evita erro de índice
                        if c - 1 >= len(header):
                            continue

                        visitante = header[c - 1]

                        # Escreve no CSV
                        writer.writerow([mandante, placar, visitante, ANO])

                continue  # pula para próxima tabela

            # =========================
            # TRATAMENTO PADRÃO (OUTRAS TABELAS)
            # =========================
            rowspan_map = {}  # controla células com rowspan
            ref_index = None  # índice da coluna "Ref."

            rows = table.find_all("tr")

            # Percorre cada linha da tabela
            for r, row in enumerate(rows):
                cols = []
                col_index = 0

                # Percorre células da linha
                for cell in row.find_all(["td", "th"]):

                    # Preenche valores pendentes de rowspan
                    while (r, col_index) in rowspan_map:
                        cols.append(rowspan_map[(r, col_index)])
                        col_index += 1

                    # Extrai texto da célula
                    text = cell.get_text(strip=True)

                    # Verifica rowspan e colspan
                    rowspan = int(cell.get("rowspan", 1))
                    colspan = int(cell.get("colspan", 1))

                    # Repete valores conforme colspan
                    for _ in range(colspan):
                        cols.append(text)

                        # Salva valores futuros (rowspan)
                        if rowspan > 1:
                            for i_row in range(1, rowspan):
                                rowspan_map[(r + i_row, col_index)] = text

                        col_index += 1

                # Completa linha com valores pendentes de rowspan
                while (r, col_index) in rowspan_map:
                    cols.append(rowspan_map[(r, col_index)])
                    col_index += 1

                # Se a linha tiver conteúdo
                if cols:

                    # Detecta coluna "Ref." na tabela Hat_tricks
                    if idx_padrao == 5 and r == 0:
                        for idx, col in enumerate(cols):
                            if "ref" in col.lower():
                                ref_index = idx
                                break

                    # Remove a coluna "Ref."
                    if idx_padrao == 5 and ref_index is not None and len(cols) > ref_index:
                        cols.pop(ref_index)

                    # Escreve cabeçalho apenas uma vez
                    if r == 0:
                        if not cabecalho_escrito.get(idx_padrao):
                            writer.writerow(cols + ["Ano"])
                            cabecalho_escrito[idx_padrao] = True
                    else:
                        # Escreve linha com o ano
                        writer.writerow(cols + [ANO])
    

print("Dataset unificado criado com sucesso!")