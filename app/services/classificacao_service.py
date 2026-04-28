from app.database.connection import SessionLocal
from app.database.models import Classificacao

def listar_classificacao():
    db = SessionLocal()

    dados = db.query(Classificacao).all()

    resultado = []
    for c in dados:
        resultado.append({
            "posicao": c.posicao,
            "time": c.time.nome if c.time else None,
            "pontos": c.pontos,
            "jogos": c.jogos,
            "vitorias": c.vitorias,
            "empates": c.empates,
            "derrotas": c.derrotas,
            "gols_pro": c.gols_pro,
            "gols_contra": c.gols_contra,
            "saldo": c.saldo,
            "status": c.status,
            "ano": c.ano
        })

    db.close()
    return resultado