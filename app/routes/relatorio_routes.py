from flask import Blueprint
from app.controllers.relatorio_controller import RelatorioController
from flask_jwt_extended import jwt_required

relatorio_bp = Blueprint('relatorio', __name__)

# Rotas protegidas
relatorio_bp.route('', methods=['POST'])(jwt_required()(RelatorioController.criar_relatorio))
relatorio_bp.route('/<string:relatorio_id>', methods=['GET'])(jwt_required()(RelatorioController.obter_relatorio))
relatorio_bp.route('/<string:relatorio_id>', methods=['DELETE'])(jwt_required()(RelatorioController.deletar_relatorio))
relatorio_bp.route('/grupo/<string:grupo_id>', methods=['GET'])(jwt_required()(RelatorioController.listar_relatorios_por_grupo))
relatorio_bp.route('/financeiro/grupo/<string:grupo_id>', methods=['GET'])(jwt_required()(RelatorioController.gerar_relatorio_financeiro))