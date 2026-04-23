from app.database.connection import SessionLocal
from app.database.models import Confronto

def listar_confrontos():
    db = SessionLocal()
    try:
        dados = db.query(Confronto).all()
        return [
            {
                "id": c.id,
                "mandante_id": c.mandante_id,
                "visitante_id": c.visitante_id,
                "gols_mandante": c.gols_mandante,
                "gols_visitante": c.gols_visitante,
                "ano": c.ano
            }
            for c in dados
        ]
    finally:
        db.close()