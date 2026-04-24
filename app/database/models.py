from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True)


class Confronto(Base):
    __tablename__ = "confrontos"

    id = Column(Integer, primary_key=True)
    mandante_id = Column(Integer, ForeignKey("times.id"))
    visitante_id = Column(Integer, ForeignKey("times.id"))
    gols_mandante = Column(Integer)
    gols_visitante = Column(Integer)
    ano = Column(Integer)


class Artilharia(Base):
    __tablename__ = "artilharia"

    id = Column(Integer, primary_key=True)
    posicao = Column(Integer)
    jogador = Column(String)
    time_id = Column(Integer, ForeignKey("times.id"))
    gols = Column(Integer)
    ano = Column(Integer)


class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cidade = Column(String)
    estado = Column(String)
    posicao_anterior = Column(String)
    estadio = Column(String)
    capacidade = Column(Integer)
    titulos = Column(Integer)
    ano = Column(Integer)