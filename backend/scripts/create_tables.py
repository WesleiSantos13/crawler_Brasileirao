from backend.app.database.connection import engine
from backend.app.database.models import Base

Base.metadata.create_all(bind=engine)

print("Tabelas criadas!")