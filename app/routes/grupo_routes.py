from flask import Blueprint
from app.controllers.grupo_controller import GrupoController
from flask_jwt_extended import jwt_required

grupo_bp = Blueprint('grupo', __name__)

# Rotas protegidas
grupo_bp.route('', methods=['POST'])(jwt_required()(GrupoController.criar_grupo))
grupo_bp.route('', methods=['GET'])(jwt_required()(GrupoController.listar_grupos))
grupo_bp.route('/<string:grupo_id>', methods=['GET'])(jwt_required()(GrupoController.obter_grupo))
grupo_bp.route('/<string:grupo_id>', methods=['PUT'])(jwt_required()(GrupoController.atualizar_grupo))
grupo_bp.route('/<string:grupo_id>', methods=['DELETE'])(jwt_required()(GrupoController.deletar_grupo))
grupo_bp.route('/<string:grupo_id>/usuarios', methods=['POST'])(jwt_required()(GrupoController.adicionar_usuario))
grupo_bp.route('/<string:grupo_id>/usuarios/<string:usuario_id>', methods=['DELETE'])(jwt_required()(GrupoController.remover_usuario))