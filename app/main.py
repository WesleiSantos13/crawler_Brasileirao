from flask import Flask
from app.routes.times import times_bp
from app.routes.confrontos import confrontos_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(times_bp)
    app.register_blueprint(confrontos_bp)

    return app