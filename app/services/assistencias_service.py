from app.database.connection import SessionLocal
from app.database.models import Assistencia

def listar_assistencias():
    db = SessionLocal()

    dados = db.query(Assistencia).all()

    resultado = []
    for a in dados:
        resultado.append({
            "posicao": a.posicao,
            "jogador": a.jogador,
            "time": a.time.nome if a.time else None,
            "assistencias": a.assistencias,
            "ano": a.ano
        })

    db.close()
    return resultado