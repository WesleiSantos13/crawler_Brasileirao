import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from bs4 import BeautifulSoup

# 🔹 NOVO: conexão com banco
from app.database.connection import SessionLocal, engine, Base
from app.database.models import Time, Confronto, Artilharia, Participante

# cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Lista de anos que serão coletados
anos = [2023, 2024, 2025]

# Mapeamento dos índices das tabelas para cada ano
mapa_indices = {
    2025: [1, 3, 4, 6, 7, 8],
    2024: [0, 2, 3, 5, 6, 8],
    2023: [0, 2, 3, 5, 6, 8]
}

# Mapeamento de siglas para nomes completos
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

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 🔹 conexão banco
db = SessionLocal()

# 🔹 cache de times
mapa_ids = {}

# 🔹 função helper para garantir time
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
            header = [mapa_times.get(time, time) for time in header_raw]

            for r in range(1, len(rows)):
                cells = rows[r].find_all(["td", "th"])
                mandante = cells[0].get_text(strip=True)

                for c in range(1, len(cells)):
                    placar = cells[c].get_text(strip=True).strip()

                    if not placar or all(x in "-–— " for x in placar):
                        continue

                    if c - 1 >= len(header):
                        continue

                    visitante = header[c - 1]

                    mandante_id = get_time_id(mandante)
                    visitante_id = get_time_id(visitante)

                    try:
                        g1, g2 = map(int, placar.replace("–", "x").replace("-", "x").split("x"))
                    except:
                        continue

                    confronto = Confronto(
                        mandante_id=mandante_id,
                        visitante_id=visitante_id,
                        gols_mandante=g1,
                        gols_visitante=g2,
                        ano=ANO
                    )

                    db.add(confronto)

            continue

        # =========================
        # PARTICIPANTES
        # =========================
        if idx_padrao == 0:
            rows = table.find_all("tr")

            for r in range(1, len(rows)):
                cols = [c.get_text(strip=True) for c in rows[r].find_all("td")]

                if len(cols) < 7:
                    continue

                nome = cols[0]
                cidade = cols[1]
                estado = cols[2]
                pos_anterior = cols[3]
                estadio = cols[4]
                capacidade = cols[5]

                try:
                    titulos = int(cols[6])
                except:
                    titulos = 0

                time_id = get_time_id(nome)

                participante = Participante(
                    time_id=time_id,
                    cidade=cidade,
                    estado=estado,
                    posicao_anterior=pos_anterior,
                    estadio=estadio,
                    capacidade=capacidade,
                    titulos=titulos,
                    ano=ANO
                )

                db.add(participante)

            continue

        # =========================
        # ARTILHARIA
        # =========================
        if idx_padrao == 3:
            rows = table.find_all("tr")

            for r in range(1, len(rows)):
                cols = [c.get_text(strip=True) for c in rows[r].find_all("td")]

                if len(cols) < 4:
                    continue

                try:
                    pos = int(cols[0])
                    jogador = cols[1]
                    time = cols[2]
                    gols = int(cols[3])
                except:
                    continue

                time_id = get_time_id(time)

                registro = Artilharia(
                    posicao=pos,
                    jogador=jogador,
                    time_id=time_id,
                    gols=gols,
                    ano=ANO
                )

                db.add(registro)

            continue


print("Inserindo no banco...")

db.commit()
db.close()

print("Dados inseridos com sucesso!")