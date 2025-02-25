from app.models.regra_casa import RegraCasa
from app.models.grupo_republica import GrupoRepublica
from app.models.usuario import Usuario
from app.models.notificacao import Notificacao
from flask import jsonify, request
from bson import ObjectId

class RegraController:
    @staticmethod
    def criar_regra():
        data = request.get_json()
        
        # Verificar se o grupo existe
        grupo_id = data.get("grupo_id")
        grupo = GrupoRepublica.find_by_id(grupo_id)
        if not grupo:
            return jsonify({"error": "Grupo não encontrado"}), 404
        
        # Verificar se o usuário existe e pertence ao grupo
        criado_por = data.get("criado_por")
        usuario = Usuario.find_by_id(criado_por)
        if not usuario or usuario.get("grupo_id") != grupo_id:
            return jsonify({"error": "Usuário não encontrado no grupo"}), 404
        
        # Criar nova regra
        try:
            regra = RegraCasa.from_dict(data)
            regra_id = regra.save()
            
            # Notificar todos os moradores sobre a nova regra
            usuarios = Usuario.find_by_grupo(grupo_id)
            for u in usuarios:
                if str(u.get("_id")) != criado_por:  # Não notificar o criador
                    notificacao = Notificacao(
                        titulo=f"Nova regra da casa: {data.get('titulo')}",
                        mensagem=f"Uma nova regra foi adicionada: {data.get('titulo')}. Acesse para mais detalhes.",
                        usuario_id=str(u.get("_id")),
                        tipo="sistema",
                        referencia_id=regra_id,
                        grupo_id=grupo_id
                    )
                    notificacao.save()
            
            return jsonify({
                "message": "Regra criada com sucesso",
                "regra_id": regra_id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def obter_regra(regra_id):
        try:
            regra = RegraCasa.find_by_id(regra_id)
            if not regra:
                return jsonify({"error": "Regra não encontrada"}), 404
            
            return jsonify(regra), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def atualizar_regra(regra_id):
        data = request.get_json()
        
        try:
            # Verificar se a regra existe
            regra = RegraCasa.find_by_id(regra_id)
            if not regra:
                return jsonify({"error": "Regra não encontrada"}), 404
            
            # Atualizar regra
            success = RegraCasa.update(regra_id, data)
            if success:
                # Notificar os moradores sobre a alteração
                if "titulo" in data or "descricao" in data:
                    usuarios = Usuario.find_by_grupo(regra.get("grupo_id"))
                    for u in usuarios:
                        notificacao = Notificacao(
                            titulo=f"Regra atualizada: {regra.get('titulo')}",
                            mensagem=f"Uma regra da casa foi atualizada. Acesse para ver as mudanças.",
                            usuario_id=str(u.get("_id")),
                            tipo="sistema",
                            referencia_id=regra_id,
                            grupo_id=regra.get("grupo_id")
                        )
                        notificacao.save()
                
                return jsonify({"message": "Regra atualizada com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao atualizar regra"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def deletar_regra(regra_id):
        try:
            # Verificar se a regra existe
            regra = RegraCasa.find_by_id(regra_id)
            if not regra:
                return jsonify({"error": "Regra não encontrada"}), 404
            
            # Deletar regra (soft delete)
            success = RegraCasa.delete(regra_id)
            if success:
                # Notificar os moradores sobre a remoção
                usuarios = Usuario.find_by_grupo(regra.get("grupo_id"))
                for u in usuarios:
                    notificacao = Notificacao(
                        titulo=f"Regra removida: {regra.get('titulo')}",
                        mensagem=f"Uma regra da casa foi removida: {regra.get('titulo')}.",
                        usuario_id=str(u.get("_id")),
                        tipo="sistema",
                        referencia_id=regra_id,
                        grupo_id=regra.get("grupo_id")
                    )
                    notificacao.save()
                
                return jsonify({"message": "Regra removida com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao remover regra"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_regras_por_grupo(grupo_id):
        try:
            regras = RegraCasa.find_by_grupo(grupo_id)
            return jsonify(regras), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_regras_por_categoria(grupo_id, categoria):
        try:
            regras = RegraCasa.find_by_categoria(grupo_id, categoria)
            return jsonify(regras), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500