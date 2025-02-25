from flask import Blueprint
from app.controllers.regra_controller import RegraController
from flask_jwt_extended import jwt_required

regra_bp = Blueprint('regra', __name__)

# Rotas protegidas
regra_bp.route('', methods=['POST'])(jwt_required()(RegraController.criar_regra))
regra_bp.route('/<string:regra_id>', methods=['GET'])(jwt_required()(RegraController.obter_regra))
regra_bp.route('/<string:regra_id>', methods=['PUT'])(jwt_required()(RegraController.atualizar_regra))
regra_bp.route('/<string:regra_id>', methods=['DELETE'])(jwt_required()(RegraController.deletar_regra))
regra_bp.route('/grupo/<string:grupo_id>', methods=['GET'])(jwt_required()(RegraController.listar_regras_por_grupo))
regra_bp.route('/grupo/<string:grupo_id>/categoria/<string:categoria>', methods=['GET'])(jwt_required()(RegraController.listar_regras_por_categoria))