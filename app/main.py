from flask import Flask

from app.routes.confrontos_routes import confrontos_bp
from app.routes.times_routes import times_bp
from app.routes.participantes_routes import participantes_bp
from app.routes.artilharia_routes import artilharia_bp
from app.routes.assistencias_routes import assistencias_bp
from app.routes.hattricks_routes import hattricks_bp
from app.routes.classificacao_routes import classificacao_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(confrontos_bp)
    app.register_blueprint(times_bp)
    app.register_blueprint(participantes_bp)
    app.register_blueprint(artilharia_bp)
    app.register_blueprint(assistencias_bp)
    app.register_blueprint(hattricks_bp)
    app.register_blueprint(classificacao_bp)


    return app