from app.database.connection import SessionLocal
from app.database.models import Time

def listar_times():
    db = SessionLocal()
    try:
        times = db.query(Time).all()
        return [{"id": t.id, "nome": t.nome} for t in times]
    finally:
        db.close()