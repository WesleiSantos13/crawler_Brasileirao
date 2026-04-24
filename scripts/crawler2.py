import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from bs4 import BeautifulSoup



#  NOVO: conexão com banco
from app.database.connection import SessionLocal
from app.database.models import Time, Confronto

from app.database.connection import engine, Base

# 🔥 cria as tabelas no banco
Base.metadata.create_all(bind=engine)




# Lista de anos que serão coletados
anos = [2023, 2024, 2025]

# Mapeamento dos índices das tabelas para cada ano
# (porque a posição das tabelas muda na Wikipedia)
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


# Header para evitar bloqueio do request (simula navegador)
headers = {
    "User-Agent": "Mozilla/5.0"
}

#  NOVO: conexão banco
db = SessionLocal()

#  NOVO: cache de times para evitar duplicação
mapa_ids = {}

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

        # =========================
        # TRATAMENTO IMPORTANTE: TABELA DE CONFRONTOS
        # =========================
        if idx_padrao == 2:
            rows = table.find_all("tr")

            # Primeira linha contém os times visitantes
            header_raw = [th.get_text(strip=True) for th in rows[0].find_all("th")][1:]

            # Converte sigla → nome completo
            header = [mapa_times.get(time, time) for time in header_raw]

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

                    #  NOVO: criar times se não existirem
                    for nome in [mandante, visitante]:
                        if nome not in mapa_ids:
                            existente = db.query(Time).filter_by(nome=nome).first()
                            if existente:
                                mapa_ids[nome] = existente.id
                            else:
                                novo = Time(nome=nome)
                                db.add(novo)
                                db.flush()
                                mapa_ids[nome] = novo.id

                    #  NOVO: tratar placar
                    try:
                        g1, g2 = map(int, placar.replace("–", "x").replace("-", "x").split("x"))
                    except:
                        continue

                    #  NOVO: inserir confronto
                    confronto = Confronto(
                        mandante_id=mapa_ids[mandante],
                        visitante_id=mapa_ids[visitante],
                        gols_mandante=g1,
                        gols_visitante=g2,
                        ano=ANO
                    )

                    db.add(confronto)

            continue  # pula para próxima tabela
        
        # =========================
        # TRATAMENTO PADRÃO (OUTRAS TABELAS)
        # =========================
        # (mantido, mas não inserindo no banco ainda — você pode expandir depois)

print("Inserindo no banco...")

db.commit()
db.close()

print("Dados inseridos com sucesso!")