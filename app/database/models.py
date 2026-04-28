from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.connection import Base
from sqlalchemy.orm import relationship

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

    mandante = relationship("Time", foreign_keys=[mandante_id])
    visitante = relationship("Time", foreign_keys=[visitante_id])


class Artilharia(Base):
    __tablename__ = "artilharia"

    id = Column(Integer, primary_key=True)
    posicao = Column(Integer)
    jogador = Column(String)
    time_id = Column(Integer, ForeignKey("times.id"))
    gols = Column(Integer)
    ano = Column(Integer)
    time = relationship("Time")


class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True)
    time_id = Column(Integer, ForeignKey("times.id"))
    cidade = Column(String)
    estado = Column(String)
    posicao_anterior = Column(String)
    estadio = Column(String)
    capacidade = Column(String)
    titulos = Column(Integer)
    ano = Column(Integer)

    time = relationship("Time")


class Assistencia(Base):
    __tablename__ = "assistencias"

    id = Column(Integer, primary_key=True)
    posicao = Column(Integer)
    jogador = Column(String)
    time_id = Column(Integer, ForeignKey("times.id"))
    assistencias = Column(Integer)
    ano = Column(Integer)

    time = relationship("Time")


class HatTrick(Base):
    __tablename__ = "hat_tricks"

    id = Column(Integer, primary_key=True)
    jogador = Column(String)
    time_id = Column(Integer, ForeignKey("times.id"))
    adversario_id = Column(Integer, ForeignKey("times.id"))
    gols_time = Column(Integer)
    gols_adversario = Column(Integer)
    data = Column(String)
    ano = Column(Integer)

    time = relationship("Time", foreign_keys=[time_id])
    adversario = relationship("Time", foreign_keys=[adversario_id])


class Classificacao(Base):
    __tablename__ = "classificacao"

    id = Column(Integer, primary_key=True)
    posicao = Column(Integer)
    time_id = Column(Integer, ForeignKey("times.id"))
    pontos = Column(Integer)
    jogos = Column(Integer)
    vitorias = Column(Integer)
    empates = Column(Integer)
    derrotas = Column(Integer)
    gols_pro = Column(Integer)
    gols_contra = Column(Integer)
    saldo = Column(String)
    situacao = Column(String)
    ano = Column(Integer)

    time = relationship("Time")