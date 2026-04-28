from app.database.connection import SessionLocal
from app.database.models import HatTrick

def listar_hattricks():
    db = SessionLocal()

    dados = db.query(HatTrick).all()

    resultado = []
    for h in dados:
        resultado.append({
            "jogador": h.jogador,
            "time": h.time.nome if h.time else None,
            "adversario": h.adversario.nome if h.adversario else None,
            "placar": f"{h.gols_time}x{h.gols_adversario}",  
            "data": h.data,
            "ano": h.ano
        })

    db.close()
    return resultado