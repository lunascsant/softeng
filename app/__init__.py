from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from app.config import config

mongo = PyMongo()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    mongo.init_app(app)
    jwt.init_app(app)
    
    # Registrar blueprints
    from app.routes.usuario_routes import usuario_bp
    from app.routes.grupo_routes import grupo_bp
    from app.routes.tarefa_routes import tarefa_bp
    from app.routes.despesa_routes import despesa_bp
    from app.routes.relatorio_routes import relatorio_bp
    from app.routes.regra_routes import regra_bp
    
    app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
    app.register_blueprint(grupo_bp, url_prefix='/api/grupos')
    app.register_blueprint(tarefa_bp, url_prefix='/api/tarefas')
    app.register_blueprint(despesa_bp, url_prefix='/api/despesas')
    app.register_blueprint(relatorio_bp, url_prefix='/api/relatorios')
    app.register_blueprint(regra_bp, url_prefix='/api/regras')
    
    return app