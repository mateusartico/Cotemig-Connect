from flask import Flask
from config.config import config
from app.models.database import db

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar blueprints
    from app.controllers.main_controller import main_bp
    from app.controllers.auth_controller import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app