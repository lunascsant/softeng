from datetime import datetime
from app import mongo
from bson import ObjectId

class RegraCasa:
    def __init__(self, titulo, descricao, grupo_id, criado_por, categoria=None):
        self.titulo = titulo
        self.descricao = descricao
        self.grupo_id = grupo_id
        self.criado_por = criado_por
        self.categoria = categoria  # limpeza, visitas, horarios, etc.
        self.data_criacao = datetime.utcnow()
        self.ultima_atualizacao = datetime.utcnow()
        self.status = "ativa"
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "grupo_id": self.grupo_id,
            "criado_por": self.criado_por,
            "categoria": self.categoria,
            "data_criacao": self.data_criacao,
            "ultima_atualizacao": self.ultima_atualizacao,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(data):
        regra = RegraCasa(
            titulo=data.get("titulo"),
            descricao=data.get("descricao"),
            grupo_id=data.get("grupo_id"),
            criado_por=data.get("criado_por"),
            categoria=data.get("categoria")
        )
        return regra
    
    @staticmethod
    def find_by_id(regra_id):
        regra_data = mongo.db.regras.find_one({"_id": ObjectId(regra_id)})
        if not regra_data:
            return None
        return regra_data
    
    @staticmethod
    def find_by_grupo(grupo_id):
        regras = mongo.db.regras.find({"grupo_id": grupo_id, "status": "ativa"})
        return list(regras)
    
    @staticmethod
    def find_by_categoria(grupo_id, categoria):
        regras = mongo.db.regras.find({"grupo_id": grupo_id, "categoria": categoria, "status": "ativa"})
        return list(regras)
    
    def save(self):
        regra_dict = self.to_dict()
        result = mongo.db.regras.insert_one(regra_dict)
        return str(result.inserted_id)
    
    @staticmethod
    def update(regra_id, update_data):
        update_data["ultima_atualizacao"] = datetime.utcnow()
        result = mongo.db.regras.update_one(
            {"_id": ObjectId(regra_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(regra_id):
        # Soft delete - apenas marca como inativa
        result = mongo.db.regras.update_one(
            {"_id": ObjectId(regra_id)},
            {"$set": {"status": "inativa", "ultima_atualizacao": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def hard_delete(regra_id):
        # Exclusão permanente
        result = mongo.db.regras.delete_one({"_id": ObjectId(regra_id)})
        return result.deleted_count > 0