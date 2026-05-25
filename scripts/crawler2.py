import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from bs4 import BeautifulSoup

#  conexão com banco
from app.database.connection import SessionLocal, engine, Base
from app.database.models import Time, Confronto, Artilharia, Participante, Assistencia, HatTrick, Classificacao

# recria tabelas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

anos = [2023, 2024, 2025]

mapa_indices = {
    2025: [1, 3, 4, 6, 7, 8],
    2024: [0, 2, 3, 5, 6, 8],
    2023: [0, 2, 3, 5, 6, 8]
}

mapa_times = {
    "AMM": "América Mineiro",
    "ATP": "Athletico Paranaense",
    "ATM": "Atlético Mineiro",
    "ATG": "Atlético Goianiense",
    "BAH": "Bahia",
    "BOT": "Botafogo",
    "COR": "Corinthians",
    "CTB": "Coritiba",
    "CRU": "Cruzeiro",
    "CUI": "Cuiabá",
    "FLA": "Flamengo",
    "FLU": "Fluminense",
    "FOR": "Fortaleza",
    "GOI": "Goiás",
    "GRE": "Grêmio",
    "INT": "Internacional",
    "PAL": "Palmeiras",
    "RBB": "Red Bull Bragantino",
    "SAN": "Santos",
    "SPA": "São Paulo",
    "VAS": "Vasco da Gama",
    "VIT": "Vitória",
    "CEA": "Ceará",
    "JUV": "Juventude",
    "CRI": "Criciúma",
    "MIR": "Mirassol",
    "SPT": "Sport"
}

headers = {"User-Agent": "Mozilla/5.0"}

db = SessionLocal()
mapa_ids = {}

# 🔹 helper
def get_time_id(nome):
    if nome not in mapa_ids:
        existente = db.query(Time).filter_by(nome=nome).first()
        if existente:
            mapa_ids[nome] = existente.id
        else:
            novo = Time(nome=nome)
            db.add(novo)
            db.flush()
            mapa_ids[nome] = novo.id
    return mapa_ids[nome]

#  parser com rowspan 
def parse_table(table, idx_padrao):
    rowspan_map = {}
    ref_index = None
    rows = table.find_all("tr")
    result = []

    for r, row in enumerate(rows):
        cols = []
        col_index = 0

        for cell in row.find_all(["td", "th"]):

            # Preenche rowspan pendente
            while (r, col_index) in rowspan_map:
                cols.append(rowspan_map[(r, col_index)])
                col_index += 1

            text = cell.get_text(strip=True)

            #  remove (C) e (F) nos hat-tricks
            if idx_padrao == 5:
                text = text.replace("(C)", "").replace("(F)", "").strip()

            rowspan = int(cell.get("rowspan", 1))
            colspan = int(cell.get("colspan", 1))

            for _ in range(colspan):
                cols.append(text)

                if rowspan > 1:
                    for i in range(1, rowspan):
                        rowspan_map[(r + i, col_index)] = text

                col_index += 1

        # completa rowspan restante
        while (r, col_index) in rowspan_map:
            cols.append(rowspan_map[(r, col_index)])
            col_index += 1

        # =========================
        #  TRATAMENTOS IMPORTANTES
        # =========================
        if cols:

            # remove [1], [2], etc
            cols = [col.split("[")[0].strip() for col in cols]

            # detecta coluna Ref no hat-tricks
            if idx_padrao == 5 and r == 0:
                for idx, col in enumerate(cols):
                    if "ref" in col.lower():
                        ref_index = idx
                        break

            # remove coluna Ref
            if idx_padrao == 5 and ref_index is not None and len(cols) > ref_index:
                cols.pop(ref_index)

            # corrige coluna títulos
            if idx_padrao == 0 and r > 0 and len(cols) > 6:
                cols[6] = cols[6].strip()[0] if cols[6] else cols[6]

            result.append(cols)

    return result

# =========================
# LOOP PRINCIPAL
# =========================
for ANO in anos:

    url = f"https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{ANO}_-_Série_A"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    tables = soup.find_all("table", class_="wikitable")
    indices = mapa_indices[ANO]

    for idx_padrao, i in enumerate(indices):

        if i >= len(tables):
            continue

        table = tables[i]

        # =========================
        # CONFRONTOS
        # =========================
        if idx_padrao == 2:
            rows = table.find_all("tr")

            header_raw = [th.get_text(strip=True) for th in rows[0].find_all("th")][1:]
            header = [mapa_times.get(t, t) for t in header_raw]

            for r in range(1, len(rows)):
                cells = rows[r].find_all(["td", "th"])
                mandante = cells[0].get_text(strip=True)

                for c in range(1, len(cells)):
                    placar = cells[c].get_text(strip=True)

                    if not placar or all(x in "-–— " for x in placar):
                        continue

                    if c - 1 >= len(header):
                        continue

                    visitante = header[c - 1]

                    try:
                        g1, g2 = map(int, placar.replace("–", "x").replace("-", "x").split("x"))
                    except:
                        continue

                    db.add(Confronto(
                        mandante_id=get_time_id(mandante),
                        visitante_id=get_time_id(visitante),
                        gols_mandante=g1,
                        gols_visitante=g2,
                        ano=ANO
                    ))

            continue

        # =========================
        # OUTRAS TABELAS (COM ROWSPAN)
        # =========================
        data = parse_table(table, idx_padrao)

        if len(data) < 2:
            continue

        header = data[0]

        # =========================
        # PARTICIPANTES
        # =========================
        if idx_padrao == 0:
            for row in data[1:]:

                if len(row) < 7:
                    continue

                nome = row[0]
                cidade = row[1]
                estado = row[2]
                pos = row[3]
                estadio = row[4]
                capacidade = row[5]

                try:
                    titulos = int(row[6])
                except:
                    titulos = 0

                db.add(Participante(
                    time_id=get_time_id(nome),
                    cidade=cidade,
                    estado=estado,
                    posicao_anterior=pos,
                    estadio=estadio,
                    capacidade=capacidade,
                    titulos=titulos,
                    ano=ANO
                ))

        # =========================
        # ARTILHARIA
        # =========================
        if idx_padrao == 3:
            for row in data[1:]:

                if len(row) < 4:
                    continue

                try:
                    pos = int(row[0])
                    jogador = row[1]
                    time = row[2]
                    gols = int(row[3])
                except:
                    continue

                db.add(Artilharia(
                    posicao=pos,
                    jogador=jogador,
                    time_id=get_time_id(time),
                    gols=gols,
                    ano=ANO
                ))
        
        # =========================
        # ASSISTENCIAS
        # =========================
        if idx_padrao == 4:
            for row in data[1:]:

                if len(row) < 4:
                    continue

                try:
                    pos = int(row[0])
                    jogador = row[1]
                    time = row[2]
                    assists = int(row[3])
                except:
                    continue

                db.add(Assistencia(
                    posicao=pos,
                    jogador=jogador,
                    time_id=get_time_id(time),
                    assistencias=assists,
                    ano=ANO
                ))        

        # =========================
        # HAT-TRICKS
        # =========================
        if idx_padrao == 5:
            for row in data[1:]:

                if len(row) < 5:
                    continue

                jogador = row[0]
                time = row[1]
                adversario = row[2]
                placar = row[3].replace("(C)", "").replace("(F)", "").strip()
                data_jogo = row[4]

                try:
                    g1, g2 = map(int, placar.replace("–", "x").replace("-", "x").split("x"))
                except:
                    continue

                db.add(HatTrick(
                    jogador=jogador,
                    time_id=get_time_id(time),
                    adversario_id=get_time_id(adversario),
                    gols_time=g1,
                    gols_adversario=g2,
                    data=data_jogo,
                    ano=ANO
                ))
        
        # =========================
        # CLASSIFICACAO
        # =========================
        if idx_padrao == 1:
            for row in data[1:]:

                if len(row) < 10:
                    continue

                try:
                    pos = int(row[0])
                except:
                    continue

                # limpa nome do time (remove (C), (R), etc)
                time = row[1].replace("(C)", "").replace("(R)", "").strip()

                try:
                    pontos = int(row[2])
                    jogos = int(row[3])
                    vitorias = int(row[4])
                    empates = int(row[5])
                    derrotas = int(row[6])
                    gp = int(row[7])
                    gc = int(row[8])
                    saldo = row[9]
                except:
                    continue

                situacao = row[10] if len(row) > 10 else ""

                db.add(Classificacao(
                    posicao=pos,
                    time_id=get_time_id(time),
                    pontos=pontos,
                    jogos=jogos,
                    vitorias=vitorias,
                    empates=empates,
                    derrotas=derrotas,
                    gols_pro=gp,
                    gols_contra=gc,
                    saldo=saldo,
                    situacao=situacao,
                    ano=ANO
                ))


print("Inserindo no banco...")
db.commit()
db.close()
print("Dados inseridos com sucesso!")