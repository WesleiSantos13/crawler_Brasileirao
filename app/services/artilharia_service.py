from app.database.connection import SessionLocal
from app.database.models import Artilharia

def listar_artilharia():
    db = SessionLocal()

    dados = db.query(Artilharia).all()

    resultado = []
    for a in dados:
        resultado.append({
            "posicao": a.posicao,
            "jogador": a.jogador,
            "time": a.time.nome if a.time else None,
            "gols": a.gols,
            "ano": a.ano
        })

    db.close()
    return resultado