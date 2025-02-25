from app.models.tarefa import Tarefa
from app.models.usuario import Usuario
from app.models.grupo_republica import GrupoRepublica
from app.models.notificacao import Notificacao
from flask import jsonify, request
from bson import ObjectId
from datetime import datetime

class TarefaController:
    @staticmethod
    def criar_tarefa():
        data = request.get_json()
        
        # Verificar se o grupo existe
        grupo_id = data.get("grupo_id")
        grupo = GrupoRepublica.find_by_id(grupo_id)
        if not grupo:
            return jsonify({"error": "Grupo não encontrado"}), 404
        
        # Verificar se o responsável existe e pertence ao grupo
        responsavel_id = data.get("responsavel_id")
        responsavel = Usuario.find_by_id(responsavel_id)
        if not responsavel or responsavel.get("grupo_id") != grupo_id:
            return jsonify({"error": "Responsável não encontrado no grupo"}), 404
        
        # Criar nova tarefa
        try:
            tarefa = Tarefa.from_dict(data)
            tarefa_id = tarefa.save()
            
            # Criar notificação para o responsável
            notificacao = Notificacao(
                titulo=f"Nova tarefa: {data.get('titulo')}",
                mensagem=f"Você foi designado para a tarefa: {data.get('titulo')}",
                usuario_id=responsavel_id,
                tipo="tarefa",
                referencia_id=tarefa_id,
                grupo_id=grupo_id
            )
            notificacao.save()
            
            return jsonify({
                "message": "Tarefa criada com sucesso",
                "tarefa_id": tarefa_id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def obter_tarefa(tarefa_id):
        try:
            tarefa = Tarefa.find_by_id(tarefa_id)
            if not tarefa:
                return jsonify({"error": "Tarefa não encontrada"}), 404
            
            return jsonify(tarefa), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def atualizar_tarefa(tarefa_id):
        data = request.get_json()
        
        try:
            # Verificar se a tarefa existe
            tarefa = Tarefa.find_by_id(tarefa_id)
            if not tarefa:
                return jsonify({"error": "Tarefa não encontrada"}), 404
            
            # Se estiver alterando o responsável, verificar se o novo responsável existe
            if "responsavel_id" in data and data.get("responsavel_id") != tarefa.get("responsavel_id"):
                responsavel_id = data.get("responsavel_id")
                responsavel = Usuario.find_by_id(responsavel_id)
                if not responsavel or responsavel.get("grupo_id") != tarefa.get("grupo_id"):
                    return jsonify({"error": "Novo responsável não encontrado no grupo"}), 404
                
                # Criar notificação para o novo responsável
                notificacao = Notificacao(
                    titulo=f"Responsabilidade por tarefa: {tarefa.get('titulo')}",
                    mensagem=f"Você foi designado como novo responsável pela tarefa: {tarefa.get('titulo')}",
                    usuario_id=responsavel_id,
                    tipo="tarefa",
                    referencia_id=tarefa_id,
                    grupo_id=tarefa.get("grupo_id")
                )
                notificacao.save()
            
            # Atualizar tarefa
            success = Tarefa.update(tarefa_id, data)
            if success:
                # Se a tarefa foi concluída, criar notificação para o grupo
                if data.get("status") == "concluida":
                    # Criar notificação para todos os membros do grupo
                    usuarios = Usuario.find_by_grupo(tarefa.get("grupo_id"))
                    for usuario in usuarios:
                        notificacao = Notificacao(
                            titulo=f"Tarefa concluída: {tarefa.get('titulo')}",
                            mensagem=f"A tarefa '{tarefa.get('titulo')}' foi marcada como concluída.",
                            usuario_id=str(usuario.get("_id")),
                            tipo="tarefa",
                            referencia_id=tarefa_id,
                            grupo_id=tarefa.get("grupo_id")
                        )
                        notificacao.save()
                
                return jsonify({"message": "Tarefa atualizada com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao atualizar tarefa"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def deletar_tarefa(tarefa_id):
        try:
            # Verificar se a tarefa existe
            tarefa = Tarefa.find_by_id(tarefa_id)
            if not tarefa:
                return jsonify({"error": "Tarefa não encontrada"}), 404
            
            # Deletar tarefa
            success = Tarefa.delete(tarefa_id)
            if success:
                return jsonify({"message": "Tarefa deletada com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao deletar tarefa"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_tarefas_por_grupo(grupo_id):
        try:
            tarefas = Tarefa.find_by_grupo(grupo_id)
            return jsonify(tarefas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_tarefas_por_responsavel(usuario_id):
        try:
            tarefas = Tarefa.find_by_responsavel(usuario_id)
            return jsonify(tarefas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_tarefas_proximas(grupo_id):
        try:
            dias = request.args.get("dias", 7, type=int)
            tarefas = Tarefa.listar_tarefas_proximas(grupo_id, dias)
            return jsonify(tarefas), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500