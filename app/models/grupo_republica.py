from datetime import datetime
from app import mongo
from bson import ObjectId

class GrupoRepublica:
    def __init__(self, nome, endereco, admin_id, max_moradores=10, descricao=None):
        self.nome = nome
        self.endereco = endereco
        self.admin_id = admin_id
        self.max_moradores = max_moradores
        self.descricao = descricao
        self.data_criacao = datetime.utcnow()
        self.status = "ativo"
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "endereco": self.endereco,
            "admin_id": self.admin_id,
            "max_moradores": self.max_moradores,
            "descricao": self.descricao,
            "data_criacao": self.data_criacao,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(data):
        grupo = GrupoRepublica(
            nome=data.get("nome"),
            endereco=data.get("endereco"),
            admin_id=data.get("admin_id"),
            max_moradores=data.get("max_moradores", 10),
            descricao=data.get("descricao")
        )
        return grupo
    
    @staticmethod
    def find_by_id(grupo_id):
        grupo_data = mongo.db.grupos.find_one({"_id": ObjectId(grupo_id)})
        if not grupo_data:
            return None
        return grupo_data
    
    @staticmethod
    def find_by_admin(admin_id):
        grupos = mongo.db.grupos.find({"admin_id": admin_id})
        return list(grupos)
    
    def save(self):
        grupo_dict = self.to_dict()
        result = mongo.db.grupos.insert_one(grupo_dict)
        return str(result.inserted_id)
    
    @staticmethod
    def update(grupo_id, update_data):
        result = mongo.db.grupos.update_one(
            {"_id": ObjectId(grupo_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(grupo_id):
        result = mongo.db.grupos.delete_one({"_id": ObjectId(grupo_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def contar_usuarios(grupo_id):
        return mongo.db.usuarios.count_documents({"grupo_id": grupo_id})
    
    @staticmethod
    def listar_todos():
        grupos = mongo.db.grupos.find({"status": "ativo"})
        return list(grupos)