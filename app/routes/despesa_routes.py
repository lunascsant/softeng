from flask import Blueprint
from app.controllers.despesa_controller import DespesaController
from flask_jwt_extended import jwt_required

despesa_bp = Blueprint('despesa', __name__)

# Rotas protegidas
despesa_bp.route('', methods=['POST'])(jwt_required()(DespesaController.criar_despesa))
despesa_bp.route('/<string:despesa_id>', methods=['GET'])(jwt_required()(DespesaController.obter_despesa))
despesa_bp.route('/<string:despesa_id>', methods=['PUT'])(jwt_required()(DespesaController.atualizar_despesa))
despesa_bp.route('/<string:despesa_id>', methods=['DELETE'])(jwt_required()(DespesaController.deletar_despesa))
despesa_bp.route('/grupo/<string:grupo_id>', methods=['GET'])(jwt_required()(DespesaController.listar_despesas_por_grupo))
despesa_bp.route('/participante/<string:usuario_id>', methods=['GET'])(jwt_required()(DespesaController.listar_despesas_por_participante))
despesa_bp.route('/grupo/<string:grupo_id>/categoria/<string:categoria>', methods=['GET'])(jwt_required()(DespesaController.listar_despesas_por_categoria))
despesa_bp.route('/grupo/<string:grupo_id>/totais', methods=['GET'])(jwt_required()(DespesaController.obter_total_por_categoria))