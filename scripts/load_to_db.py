import pandas as pd
from app.database.connection import SessionLocal
from app.database.models import Time, Confronto

db = SessionLocal()

df = pd.read_csv("data/Confrontos.csv")

# 🔹 Buscar times já existentes
times_existentes = {t.nome: t.id for t in db.query(Time).all()}

# 🔹 Criar novos times sem duplicar
mapa_ids = {}

for nome in set(df["Mandante"]).union(set(df["Visitante"])):
    if nome in times_existentes:
        mapa_ids[nome] = times_existentes[nome]
    else:
        time = Time(nome=nome)
        db.add(time)
        db.flush()  # pega ID sem commit
        mapa_ids[nome] = time.id

# 🔹 Inserir confrontos
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

# 🔹 Um único commit
db.commit()
db.close()

print("Dados inseridos!")