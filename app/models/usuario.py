from datetime import datetime
from app import mongo
from bson import ObjectId
import bcrypt

class Usuario:
    def __init__(self, nome, email, telefone, senha, foto=None, tipo="padrao", grupo_id=None):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha_hash = self._hash_password(senha)
        self.foto = foto
        self.tipo = tipo  # admin, padrao, convidado
        self.grupo_id = grupo_id
        self.data_criacao = datetime.utcnow()
        self.status = "ativo"

    def _hash_password(self, senha):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')
    
    def verificar_senha(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "senha_hash": self.senha_hash,
            "telefone": self.telefone,
            "foto": self.foto,
            "tipo": self.tipo,
            "grupo_id": self.grupo_id,
            "data_criacao": self.data_criacao,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(data):
        usuario = Usuario(
            nome=data.get("nome"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            senha=data.get("senha"),
            foto=data.get("foto"),
            tipo=data.get("tipo", "padrao"),
            grupo_id=data.get("grupo_id")
        )
        return usuario
    
    @staticmethod
    def find_by_id(usuario_id):
        usuario_data = mongo.db.usuarios.find_one({"_id": ObjectId(usuario_id)})
        if not usuario_data:
            return None
        return usuario_data
    
    @staticmethod
    def find_by_email(email):
        usuario_data = mongo.db.usuarios.find_one({"email": email})
        if not usuario_data:
            return None
        return usuario_data
    
    @staticmethod
    def find_by_grupo(grupo_id):
        usuarios = mongo.db.usuarios.find({"grupo_id": grupo_id})
        return list(usuarios)
    
    def save(self):
        usuario_dict = self.to_dict()
        result = mongo.db.usuarios.insert_one(usuario_dict)
        return str(result.inserted_id)
    
    @staticmethod
    def update(usuario_id, update_data):
        # Remover senha do dicionário de atualização se estiver presente
        if "senha" in update_data:
            senha = update_data.pop("senha")
            update_data["senha_hash"] = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        result = mongo.db.usuarios.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(usuario_id):
        result = mongo.db.usuarios.delete_one({"_id": ObjectId(usuario_id)})
        return result.deleted_count > 0