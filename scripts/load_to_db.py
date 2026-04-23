import pandas as pd
from app.database.connection import SessionLocal
from app.database.models import Time, Confronto

db = SessionLocal()

df = pd.read_csv("data/raw/Confrontos.csv")

times = set(df["Mandante"]).union(set(df["Visitante"]))

mapa_ids = {}

for nome in times:
    time = Time(nome=nome)
    db.add(time)
    db.commit()
    db.refresh(time)
    mapa_ids[nome] = time.id

for _, row in df.iterrows():
    try:
        g1, g2 = map(int, row["Placar"].replace("–", "x").replace("-", "x").split("x"))
    except:
        continue

    confronto = Confronto(
        mandante_id=mapa_ids[row["Mandante"]],
        visitante_id=mapa_ids[row["Visitante"]],
        gols_mandante=g1,
        gols_visitante=g2,
        ano=int(row["Ano"])
    )

    db.add(confronto)

db.commit()
db.close()

print("Dados inseridos!")