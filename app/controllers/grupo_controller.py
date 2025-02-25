from app.models.grupo_republica import GrupoRepublica
from app.models.usuario import Usuario
from flask import jsonify, request
from bson import ObjectId

class GrupoController:
    @staticmethod
    def criar_grupo():
        data = request.get_json()
        
        # Verificar se o admin_id existe
        admin_id = data.get("admin_id")
        admin = Usuario.find_by_id(admin_id)
        if not admin:
            return jsonify({"error": "Administrador não encontrado"}), 404
        
        # Criar novo grupo
        try:
            grupo = GrupoRepublica.from_dict(data)
            grupo_id = grupo.save()
            
            # Atualizar o usuário admin para associá-lo ao grupo
            Usuario.update(admin_id, {"grupo_id": grupo_id, "tipo": "admin"})
            
            return jsonify({
                "message": "Grupo criado com sucesso",
                "grupo_id": grupo_id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def obter_grupo(grupo_id):
        try:
            grupo = GrupoRepublica.find_by_id(grupo_id)
            if not grupo:
                return jsonify({"error": "Grupo não encontrado"}), 404
            
            return jsonify(grupo), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def atualizar_grupo(grupo_id):
        data = request.get_json()
        
        try:
            # Verificar se o grupo existe
            grupo = GrupoRepublica.find_by_id(grupo_id)
            if not grupo:
                return jsonify({"error": "Grupo não encontrado"}), 404
            
            # Atualizar grupo
            success = GrupoRepublica.update(grupo_id, data)
            if success:
                return jsonify({"message": "Grupo atualizado com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao atualizar grupo"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def deletar_grupo(grupo_id):
        try:
            # Verificar se o grupo existe
            grupo = GrupoRepublica.find_by_id(grupo_id)
            if not grupo:
                return jsonify({"error": "Grupo não encontrado"}), 404
            
            # Deletar grupo
            success = GrupoRepublica.delete(grupo_id)
            if success:
                # Remover associação do grupo de todos os usuários
                mongo.db.usuarios.update_many(
                    {"grupo_id": grupo_id},
                    {"$unset": {"grupo_id": ""}}
                )
                
                return jsonify({"message": "Grupo deletado com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao deletar grupo"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def adicionar_usuario(grupo_id):
        data = request.get_json()
        usuario_id = data.get("usuario_id")
        tipo = data.get("tipo", "padrao")
        
        try:
            # Verificar se o grupo existe
            grupo = GrupoRepublica.find_by_id(grupo_id)
            if not grupo:
                return jsonify({"error": "Grupo não encontrado"}), 404
            
            # Verificar se o usuário existe
            usuario = Usuario.find_by_id(usuario_id)
            if not usuario:
                return jsonify({"error": "Usuário não encontrado"}), 404
            
            # Verificar se já atingiu o limite de moradores
            num_moradores = GrupoRepublica.contar_usuarios(grupo_id)
            if num_moradores >= grupo.get("max_moradores", 10):
                return jsonify({"error": "Limite de moradores atingido"}), 400
            
            # Adicionar usuário ao grupo
            success = Usuario.update(usuario_id, {"grupo_id": grupo_id, "tipo": tipo})
            if success:
                return jsonify({"message": "Usuário adicionado ao grupo com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao adicionar usuário ao grupo"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def remover_usuario(grupo_id, usuario_id):
        try:
            # Verificar se o grupo existe
            grupo = GrupoRepublica.find_by_id(grupo_id)
            if not grupo:
                return jsonify({"error": "Grupo não encontrado"}), 404
            
            # Verificar se o usuário existe e pertence ao grupo
            usuario = Usuario.find_by_id(usuario_id)
            if not usuario or usuario.get("grupo_id") != grupo_id:
                return jsonify({"error": "Usuário não encontrado no grupo"}), 404
            
            # Verificar se o usuário é administrador
            if usuario.get("tipo") == "admin":
                return jsonify({"error": "Não é possível remover o administrador do grupo"}), 400
            
            # Remover usuário do grupo
            success = Usuario.update(usuario_id, {"$unset": {"grupo_id": ""}})
            if success:
                return jsonify({"message": "Usuário removido do grupo com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao remover usuário do grupo"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def listar_grupos():
        try:
            grupos = GrupoRepublica.listar_todos()
            return jsonify(grupos), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500