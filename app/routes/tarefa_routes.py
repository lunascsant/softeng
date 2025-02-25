from flask import Blueprint
from app.controllers.tarefa_controller import TarefaController
from flask_jwt_extended import jwt_required

tarefa_bp = Blueprint('tarefa', __name__)

# Rotas protegidas
tarefa_bp.route('', methods=['POST'])(jwt_required()(TarefaController.criar_tarefa))
tarefa_bp.route('/<string:tarefa_id>', methods=['GET'])(jwt_required()(TarefaController.obter_tarefa))
tarefa_bp.route('/<string:tarefa_id>', methods=['PUT'])(jwt_required()(TarefaController.atualizar_tarefa))
tarefa_bp.route('/<string:tarefa_id>', methods=['DELETE'])(jwt_required()(TarefaController.deletar_tarefa))
tarefa_bp.route('/grupo/<string:grupo_id>', methods=['GET'])(jwt_required()(TarefaController.listar_tarefas_por_grupo))
tarefa_bp.route('/responsavel/<string:usuario_id>', methods=['GET'])(jwt_required()(TarefaController.listar_tarefas_por_responsavel))
tarefa_bp.route('/proximas/<string:grupo_id>', methods=['GET'])(jwt_required()(TarefaController.listar_tarefas_proximas))