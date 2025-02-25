from flask import Blueprint
from app.controllers.usuario_controller import UsuarioController
from flask_jwt_extended import jwt_required

usuario_bp = Blueprint('usuario', __name__)

# Rotas públicas
usuario_bp.route('/registrar', methods=['POST'])(UsuarioController.criar_usuario)
usuario_bp.route('/login', methods=['POST'])(UsuarioController.login)

# Rotas protegidas
usuario_bp.route('/<string:usuario_id>', methods=['GET'])(jwt_required()(UsuarioController.obter_usuario))
usuario_bp.route('/<string:usuario_id>', methods=['PUT'])(jwt_required()(UsuarioController.atualizar_usuario))
usuario_bp.route('/<string:usuario_id>', methods=['DELETE'])(jwt_required()(UsuarioController.deletar_usuario))
usuario_bp.route('/grupo/<string:grupo_id>', methods=['GET'])(jwt_required()(UsuarioController.listar_usuarios_por_grupo))