from app.models.usuario import Usuario
from flask import jsonify, request
from bson import ObjectId
from app import mongo
import bcrypt
from flask_jwt_extended import create_access_token

class UsuarioController:
    @staticmethod
    def criar_usuario():
        data = request.get_json()
        
        # Verificar se o email já está em uso
        if Usuario.find_by_email(data.get("email")):
            return jsonify({"error": "Email já cadastrado"}), 400
        
        # Criar novo usuário
        try:
            usuario = Usuario.from_dict(data)
            usuario_id = usuario.save()
            
            return jsonify({
                "message": "Usuário criado com sucesso",
                "usuario_id": usuario_id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def obter_usuario(usuario_id):
        try:
            usuario = Usuario.find_by_id(usuario_id)
            if not usuario:
                return jsonify({"error": "Usuário não encontrado"}), 404
            
            # Remover senha do resultado
            if "senha_hash" in usuario:
                del usuario["senha_hash"]
            
            return jsonify(usuario), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def atualizar_usuario(usuario_id):
        data = request.get_json()
        
        try:
            # Verificar se o usuário existe
            usuario = Usuario.find_by_id(usuario_id)
            if not usuario:
                return jsonify({"error": "Usuário não encontrado"}), 404
            
            # Atualizar usuário
            success = Usuario.update(usuario_id, data)
            if success:
                return jsonify({"message": "Usuário atualizado com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao atualizar usuário"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def deletar_usuario(usuario_id):
        try:
            # Verificar se o usuário existe
            usuario = Usuario.find_by_id(usuario_id)
            if not usuario:
                return jsonify({"error": "Usuário não encontrado"}), 404
            
            # Deletar usuário
            success = Usuario.delete(usuario_id)
            if success:
                return jsonify({"message": "Usuário deletado com sucesso"}), 200
            else:
                return jsonify({"error": "Falha ao deletar usuário"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get("email")
        senha = data.get("senha")
        
        usuario = Usuario.find_by_email(email)
        if not usuario:
            return jsonify({"error": "Credenciais inválidas"}), 401

        
        print(f"Usuário encontrado: {usuario}")
        print(f"Senha hash do usuário: {usuario.get('senha_hash')}")
    
        senha_hash = usuario.get("senha_hash")
        if not senha_hash:
            return jsonify({"error": "Erro no sistema de autenticação"}), 500
        
        if bcrypt.checkpw(senha.encode('utf-8'), usuario.get("senha_hash").encode('utf-8')):
            # Gerar token JWT
            access_token = create_access_token(identity=str(usuario.get("_id")))
            
            return jsonify({
                "message": "Login realizado com sucesso",
                "access_token": access_token,
                "usuario": {
                    "id": str(usuario.get("_id")),
                    "nome": usuario.get("nome"),
                    "email": usuario.get("email"),
                    "tipo": usuario.get("tipo"),
                    "grupo_id": usuario.get("grupo_id")
                }
            }), 200
        else:
            return jsonify({"error": "Credenciais inválidas"}), 401
    
    @staticmethod
    def listar_usuarios_por_grupo(grupo_id):
        try:
            usuarios = Usuario.find_by_grupo(grupo_id)
            
            # Remover senha_hash de todos os resultados
            for usuario in usuarios:
                if "senha_hash" in usuario:
                    del usuario["senha_hash"]
            
            return jsonify(usuarios), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500